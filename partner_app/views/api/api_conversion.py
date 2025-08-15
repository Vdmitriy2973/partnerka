from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from partner_app.models import ProjectPartner, PartnerActivity, AdvertiserActivity, User, PartnerProfile,AdvertiserProfile, Platform,Project
from partner_app.serializers import ConversionSerializer

from decimal import Decimal

class ConversionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        partner = User.objects.get(id=int(request.data["partner"]))
        if partner.is_currently_blocked():
            return Response(
                {"detail": "Сотрудничество с данным партнёром на данный момент приостановлено, т.к. аккаунт партнёра заблокирован!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        referrer = request.data.get('referrer')
        if referrer:
            platform = Platform.objects.get(
                partner=request.data["partner"],
                url_or_id__contains=referrer
            )
            platform_id = platform.id
        else:
            referrer = None
            platform_id = None
            
        try:
            partnership = ProjectPartner.objects.get(
                partner=request.data["partner"],
                project=request.data["project"]
            )
            project = Project.objects.get(
                id=request.data['project']
            )
        except ProjectPartner.DoesNotExist:
            return Response(
                {"detail": "Нет такого проекта или партнёр не сотрудничает с ним!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if partnership.status != partnership.StatusType.ACTIVE:
            return Response(
                {"detail": "Сотрудничество с данным партнёром на данный момент приостановлено!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
        
        meta = None
        if 'details' in request.data:
            meta = request.data["details"]
        if not partnership:
            return Response({"detail":"Нет такого проекта или партнёр не сотрудничает с ним!"},status=status.HTTP_404_NOT_FOUND)
        
        if len(partnership.partner_links.all()) < 1:
            return Response({"detail":"Конверсия не может быть засчитана, т.к. не сгенерирована партнёрская ссылка!"},status=status.HTTP_400_BAD_REQUEST)
        
        ip = request.META.get('HTTP_X_FORWARDED_FOR',None)
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        data = {
            "project":request.data["project"],
            "partner":request.data["partner"],
            "amount":project.cost_per_action,
            "meta":meta,
            "partner_link":partnership.partner_links.first().id,
            "partnership":partnership.id,
            "platform":platform_id,
            "user_agent":request.META.get('HTTP_USER_AGENT', None),
            "ip_address":ip,
            
        }
        serializer = ConversionSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            partnership.project.advertiser.advertiserprofile.balance -= Decimal(project.cost_per_action)
            partnership.partner.partner_profile.balance += Decimal(project.cost_per_action)
            partnership.project.advertiser.advertiserprofile.save()
            partnership.partner.partner_profile.save()
            
            partnerprofile = PartnerProfile.objects.get(
                user=int(partner.id)
            )
            advertiser = User.objects.get(id=partnership.project.advertiser.id)
            adv_profile = AdvertiserProfile.objects.get(
                user=int(advertiser.id)
            )
            
            if 'details' in request.data:
                title = request.data["details"]
            else:
                title = f'Новая продажа. Проект: {partnership.project.name}'
            
            PartnerActivity.objects.create(
                partner=partnerprofile,
                activity_type='sale',
                title=title,
                details=f'Комиссия: {project.cost_per_action} ₽'
            )
            AdvertiserActivity.objects.create(
                advertiser=adv_profile,
                activity_type='sale',
                title=title,
                details=f'Комиссия: {project.cost_per_action} ₽. Партнёр: {partner.get_full_name()}'
            )
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)