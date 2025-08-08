from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from partner_app.models import ProjectPartner, Platform
from partner_app.serializers import ClickSerializer

class ClickAPIView(APIView):
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
            
        ip = request.META.get('HTTP_X_FORWARDED_FOR',None)
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        data = {
            "project":request.data["project"],
            "partner":request.data["partner"],
            "platform":platform_id,
            "partner_link":partnership.partner_links.all()[0].id,
            "partnership":partnership.id,
            "referrer":referrer,
            "user_agent":request.META.get('HTTP_USER_AGENT', None),
            "ip_address":ip,
        }
        serializer = ClickSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)