from django.db import models
from django.conf import settings
from gnw.models import Course
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

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
    is_current = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], condition=Q(is_current=True), name='unique_user_enrolled_in_current_course'),
        ]

    def clean(self):
        """
        This is called by ModelForm when saving through ModelForm (e.g. Admin site).
        Be sure to call full_clean() if creating enrollments programmatically.
        """
        if self.is_current == True:
            if Enrollment.objects.filter(user=self.user, course=self.course, is_current=True).exclude(id=self.id).exists():
                raise ValidationError(_('The user is currently enrolled in this course already.'))

    def __str__(self):
        if self.is_current:
            status = 'current'
        else:
            status = 'past'
        return self.user.username + ' ' + self.course.course_name + ' ' + status

