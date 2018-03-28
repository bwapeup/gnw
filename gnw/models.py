from django.db import models
from datetime import date


#======================================================
#Course
#======================================================
class Course(models.Model):
    course_name = models.CharField(max_length = 200, unique=True)
    slug = models.SlugField(max_length = 200, unique=True)

    def __str__(self):
        return self.course_name

#======================================================
#Unit
#======================================================
class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    unit_name = models.CharField(max_length = 200)
    unit_number = models.PositiveIntegerField()
    
    class Meta:
        unique_together = (("course", "unit_name"), ("course", "unit_number"))

    def __str__(self):
        return self.course.course_name + " " + self.unit_name


#======================================================
#Lesson
#======================================================
class Lesson(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    lesson_name = models.CharField(max_length = 200)
    lesson_number = models.PositiveIntegerField()
    
    class Meta:
        unique_together = (("unit", "lesson_name"), ("unit", "lesson_number"))

    def __str__(self):
        return self.unit.course.course_name + " Unit " + str(self.unit.unit_number) + " " + self.lesson_name


#======================================================
#Lesson_Material
#======================================================
class Lesson_Material(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)
    material_number = models.PositiveIntegerField()
    material_title = models.CharField(max_length = 50, blank=True)

    file_name = models.CharField(max_length = 200, default="#")
    random_slug = models.CharField(max_length = 6, unique=True)
    
    VIDEO = 'VD'
    DOWNLOAD = 'DL'
    MATERIAL_TYPE_CHOICES = (
        (VIDEO, 'Video'),
        (DOWNLOAD, 'Download'),
    )

    material_type = models.CharField(
        max_length=2,
        choices=MATERIAL_TYPE_CHOICES,
        default=VIDEO,
    )

    class Meta:
        unique_together = (("lesson", "material_number"))
        
    def __str__(self):
        return self.lesson.unit.course.course_name + " Unit " + str(self.lesson.unit.unit_number) + " Lesson " + str(self.lesson.lesson_number) + " LM " + str(self.material_number)

    def get_next_LM_url(self):
        #Checks to see if there are more LMs in the same lesson.
        #If yes, then get the url to go to that LM;
        #if no, then return the url to go back to the course main page
        next_LM_in_lesson = Lesson_Material.objects.filter(lesson=self.lesson, material_number__gt=self.material_number).order_by('material_number').first()
        if next_LM_in_lesson is not None:
            if next_LM_in_lesson.material_type == self.DOWNLOAD:
                next_url = next_LM_in_lesson.file_name
                next_uuid = next_LM_in_lesson.random_slug
            else:
                next_url = next_LM_in_lesson.lesson.unit.course.slug + '/' + 'lecture' + '/' + next_LM_in_lesson.random_slug + '/'
                next_uuid = next_LM_in_lesson.random_slug
        else:
            next_url = self.lesson.unit.course.slug + '/'
            next_uuid = ''
        return {'next_url':next_url, 'next_uuid':next_uuid}

