from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from partner_app.models import ProjectPartner
from partner_app.serializers import ClickSerializer

class ClickAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ClickSerializer(data=request.data)
        referer = request.META.get('HTTP_REFERER')
        if referer:
            print(f"Пользователь пришел с: {referer}")
        else:
            print("Referer не указан (прямой переход или безопасные настройки браузера)")
        partneship = ProjectPartner.objects.filter(
            partner=request.data["partner"],
            project=request.data["project"]
        )
        if not partneship.exists():
            return Response({"detail":"Нет такого проекта или партнёр не сотрудничает с ним!"},status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)