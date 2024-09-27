from cryptography.fernet import Fernet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from app.app import settings
from app.password_service.filters import ServicePasswordFilter
from app.password_service.models import ServicePassword
from app.password_service.serializers import PasswordSerializer


class PasswordAPIView(APIView):

    def post(self, request: Request, service_name: str) -> Response:
        serializer = PasswordSerializer(data={
            'password': request.data.get('password'),
            'service_name': service_name,
        })
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        password = serializer.validated_data['password']
        service_name = serializer.validated_data['service_name']
        encoder = Fernet(settings.ENCRYPTION_KEY)
        encrypted_password = encoder.encrypt(password.encode())
        service_password, created = ServicePassword.objects.update_or_create(
            service_name=service_name,
            defaults={'password': encrypted_password},
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def get(self, request: Request, service_name: str) -> Response:
        try:
            instance = ServicePassword.objects.get(service_name=service_name)
            decrypted_password = instance.get_password()
            serializer = PasswordSerializer(data={
                'password': decrypted_password,
                'service_name': service_name,
            })
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        except ServicePassword.DoesNotExist:
            return Response({'error': 'Password not found'}, status=status.HTTP_404_NOT_FOUND)


class PasswordSearchAPIView(ListAPIView):
    queryset = ServicePassword.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServicePasswordFilter

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        decrypted_passwords = []

        for service_password in queryset:
            decrypted_password = service_password.get_password()
            decrypted_passwords.append({
                'service_name': service_password.service_name,
                'password': decrypted_password,
            })
        serializer = PasswordSerializer(decrypted_passwords, many=True)
        return Response(serializer.data)
