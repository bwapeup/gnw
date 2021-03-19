from django.db import models
from django.conf import settings

class Session_Control(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='session_control')
    session_key = models.CharField(null=False, max_length=40)
