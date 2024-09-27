from cryptography.fernet import Fernet
from django.db import models
from app.app import settings


class ServicePassword(models.Model):
    service_name = models.CharField(max_length=255, unique=True)
    password = models.BinaryField()

    def get_password(self):
        encoder = Fernet(settings.ENCRYPTION_KEY)
        return encoder.decrypt(self.password.tobytes()).decode()
