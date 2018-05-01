from django.db import models
from enrollment.models import Enrollment
from gnw.models import Lesson_Material

#======================================================
#Completed Learning Materials
#======================================================
class Completed_Learning_Materials(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson_material = models.ForeignKey(Lesson_Material, on_delete=models.CASCADE)

    def __str__(self):
        if self.enrollment.is_current == True:
            status = 'current'
        else:
            status = 'past'
            
        display = self.enrollment.user.username + ' ' + self.lesson_material.lesson.unit.course.course_name + ' '
        display += ' ' + status + ' '
        display += 'unit ' + str(self.lesson_material.lesson.unit.unit_number) + ' ' + 'lesson '
        display += str(self.lesson_material.lesson.lesson_number) + ' ' + 'LM ' + str(self.lesson_material.material_number)
        return  display 
    
