from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from partner_app.models import ProjectPartner, Platform,User,PartnerProfile,AdvertiserProfile
from partner_app.serializers import ClickSerializer

class ClickAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        partner = User.objects.get(id=int(request.data["partner"]))
        partnerprofile = PartnerProfile.objects.get(
            user=int(partner.id)
        )
        
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
        if partner.is_currently_blocked():
            return Response(
                {"detail": "Сотрудничество с данным партнёром приостановлено, т.к. аккаунт партнёра заблокирован!"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
        advertiser = User.objects.get(id=partnership.project.advertiser.id)
        adv_profile = AdvertiserProfile.objects.get(
            user=int(advertiser.id)
        )
        if advertiser.is_currently_blocked():
            return Response(
                {"detail": "Сотрудничество с данным рекламодателем приостановлено, т.к. аккаунт рекламодателя заблокирован!"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if len(partnership.partner_links.all()) < 1:
            return Response({"detail":"Конверсия не может быть засчитана, т.к. не сгенерирована партнёрская ссылка!"},status=status.HTTP_400_BAD_REQUEST)
        referrer_id = request.data.get('referrer')
        if referrer_id:
            try:
                platform = Platform.objects.get(
                    id=referrer_id,
                    is_active=True
                )
                platform_id = platform.id
            except Exception:
                platform_id = None
        else:
            platform_id = None
        
        ip = request.META.get('HTTP_X_FORWARDED_FOR',None)
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        data = {
            "project":request.data["project"],
            "partner":partnerprofile.id,
            "advertiser":adv_profile.id,
            "platform":platform_id,
            "partner_link":partnership.partner_links.all()[0].id,
            "partnership":partnership.id,
            "referrer":referrer_id,
            "user_agent":request.META.get('HTTP_USER_AGENT', None),
            "ip_address":ip,
        }
        serializer = ClickSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)