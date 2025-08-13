from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProtectedAPIView(APIView):
    def get(self, request):
        return Response(
            {"message": f"Привет, {request.user.first_name} {request.user.last_name}! Вы авторизованы через API ключ."},
            status=status.HTTP_200_OK
        )