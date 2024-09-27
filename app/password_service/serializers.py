from rest_framework import serializers


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    service_name = serializers.CharField(required=True)
