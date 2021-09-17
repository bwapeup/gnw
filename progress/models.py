from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE
from django.utils.timezone import now
from enrollment.models import Enrollment
from gnw.models import Lesson, Assignment

#======================================================
#Completed Lessons
#======================================================
class Completed_Lessons(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    results = models.TextField(max_length = 10000, blank=True)
    taken = models.DateTimeField(default=now)
    assignment = models.OneToOneField(Assignment, blank=True, null=True, on_delete=CASCADE)

    def __str__(self):
        if self.enrollment.is_current == True:
            status = 'current'
        else:
            status = 'past'
            
        display = self.enrollment.user.username + ' ' + self.lesson.unit.course.course_name + ' '
        display += ' ' + status + ' '
        display += 'unit ' + str(self.lesson.unit.unit_number) + ' ' + 'lesson '
        display += str(self.lesson.lesson_number)
        return  display 

    def clean(self):
        if self.lesson.unit.course.id != self.enrollment.course.id:
            raise ValidationError('This lesson does not belong to the course associated with this enrollment.')

    def delete(self, *args, **kwargs):
        if self.assignment:
            raise models.ProtectedError(
                "There is a submitted assignment associated with this record." 
                "You can only delete this record by deleting the associated assignment.", self)
        else:
            super().delete(*args, **kwargs)
    
