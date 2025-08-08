from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from partner_app.models import ProjectPartner, PartnerActivity, AdvertiserActivity, User, PartnerProfile,AdvertiserProfile, Platform
from partner_app.serializers import ConversionSerializer

from decimal import Decimal

class ConversionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        referrer = request.META.get('HTTP_REFERER')
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
        except ProjectPartner.DoesNotExist:
            return Response(
                {"detail": "Нет такого проекта или партнёр не сотрудничает с ним!"},
                status=status.HTTP_404_NOT_FOUND
            )
        meta = None
        if 'details' in request.data:
            meta = request.data["details"]
        if not partnership:
            return Response({"detail":"Нет такого проекта или партнёр не сотрудничает с ним!"},status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "project":request.data["project"],
            "partner":request.data["partner"],
            "amount":request.data["amount"],
            "meta":meta,
            "partner_link":partnership.partner_links.all()[0].id,
            "partnership":partnership.id,
            "platform":platform_id
            
        }
        serializer = ConversionSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            partnership.project.advertiser.advertiserprofile.balance -= Decimal(request.data['amount'])
            partnership.partner.partner_profile.balance += Decimal(request.data['amount'])
            partnership.project.advertiser.advertiserprofile.save()
            partnership.partner.partner_profile.save()
            
            partner = User.objects.get(id=int(request.data["partner"]))
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
                details=f'Комиссия: {request.data["amount"]} ₽'
            )
            AdvertiserActivity.objects.create(
                advertiser=adv_profile,
                activity_type='sale',
                title=title,
                details=f'Комиссия: {request.data["amount"]} ₽. Партнёр: {partner.get_full_name()}'
            )
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)