from django.db import models
from enrollment.models import Enrollment
from gnw.models import Lesson

#======================================================
#Completed Lessons
#======================================================
class Completed_Lessons(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

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
    
