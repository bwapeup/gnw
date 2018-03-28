from django.db import models
from django.conf import settings
from gnw.models import Course
from datetime import date

#======================================================
#Enrollment_Type:
#
#Used to enforce additional logic on enrollment status
#on different users, such as trial period, special
#conditions, etc.
#======================================================
class Enrollment_Type(models.Model):
    enrollment_type = models.CharField(max_length = 100, unique=True)

    def __str__(self):
        return self.enrollment_type
    
#======================================================
#Enrollment:
#
#Used to keep track of which students are enrolled in
#which courses 
#======================================================
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    enrollment_date = models.DateField(default=date.today)
    enrollment_type = models.ForeignKey(Enrollment_Type, on_delete=models.PROTECT)

    class Meta:
        unique_together = (("user", "course"))
        
    def __str__(self):
        return self.user.username + ' ' + self.course.course_name

