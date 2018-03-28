from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


#======================================================
#BaseUser: Custom User Replacing the Django Default User
#======================================================
class CustomUser(AbstractUser):
    name = models.CharField(max_length = 100, blank=True)

    def __str__(self):
        if self.name == '':
            return self.username
        else:
            return self.name

        
#======================================================
#Student
#======================================================
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile = models.CharField(max_length = 25, blank=True)

    def __str__(self):
        if self.user.name == '':
            return self.mobile
        else:
            return self.user.name
