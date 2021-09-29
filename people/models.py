from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


#======================================================
#BaseUser: Custom User Replacing the Django Default User
#======================================================
class CustomUser(AbstractUser):
    name = models.CharField(max_length = 100, blank=True)
    mobile = models.CharField(max_length = 11, unique=True)
    require_password_change = models.BooleanField(default=False)

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
    parent_name = models.CharField(max_length = 25, blank=True)
    student_name = models.CharField(max_length = 25, blank=True)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    student_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
    )

    student_birth_date = models.DateField(null=True, blank=True, help_text='格式: 2010-08-31')
    city = models.CharField(max_length = 25, blank=True)
    staff_notes = models.TextField(max_length = 1000, blank=True)

    def __str__(self):
        if self.student_name == '':
            return self.user.mobile
        else:
            return self.student_name
