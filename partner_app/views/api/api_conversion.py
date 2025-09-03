from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from partner_app.models import ProjectPartner, PartnerActivity, AdvertiserActivity, User, PartnerProfile,AdvertiserProfile, Platform,Project
from partner_app.serializers import ConversionSerializer


class ConversionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not "partner" in request.data or not "project" in request.data:
            return Response(
                {"detail": "Параметры partner и project необходимы для выполнения запроса!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        partner = User.objects.get(id=int(request.data["partner"]))
        partnerprofile = PartnerProfile.objects.get(
            user=int(partner.id)
        )
        if partner.is_currently_blocked():
            return Response(
                {"detail": "Сотрудничество с данным партнёром на данный момент приостановлено, т.к. аккаунт партнёра заблокирован!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        referrer_id = request.data.get('referrer')
        if referrer_id:
            try:
                platform = Platform.objects.get(
                    id=referrer_id
                )
                platform_id = platform.id
            except Platform.DoesNotExist:
                platform_id = None
        else:
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
        if not project.is_active:
            return Response(
                {"detail": "На данный момент проект неактивен!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if partnership.status != partnership.StatusType.ACTIVE:
            return Response(
                {"detail": "Сотрудничество с данным партнёром на данный момент приостановлено!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
        advertiser = User.objects.get(id=partnership.project.advertiser.id)
        adv_profile = AdvertiserProfile.objects.get(
            user=int(advertiser.id)
        )
        details = ""
        if 'details' in request.data:
            details = request.data["details"]
        if not partnership:
            return Response({"detail":"Нет такого проекта или партнёр не сотрудничает с ним!"},status=status.HTTP_400_BAD_REQUEST)
        
        if len(partnership.partner_links.all()) < 1:
            return Response({"detail":"Конверсия не может быть засчитана, т.к. не сгенерирована партнёрская ссылка!"},status=status.HTTP_400_BAD_REQUEST)
        
        ip = request.META.get('HTTP_X_FORWARDED_FOR',None)
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
            
        amount = project.cost_per_action
        if 'amount' in request.data:
            if float(request.data['amount']) >= project.get_reduced_price():
                amount = request.data['amount']
        data = {
            "project":request.data["project"],
            "partner":partnerprofile.id,
            "advertiser":adv_profile.id,
            "amount":amount,
            "details":details,
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