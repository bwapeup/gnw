from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.db import models
from django.core.exceptions import ValidationError

#======================================================
#Course
#======================================================
class Course(models.Model):
    course_name = models.CharField(max_length = 200, unique=True)

    slug = models.SlugField(max_length = 200, unique=True, blank=True, help_text='Enter a URL-friendly course name without spaces and using only letters, digits, hypens, and underscores; leave it blank to auto generate from course name')

    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.course_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course_name)
        super().save(*args, **kwargs)

#======================================================
#Unit
#======================================================
class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    unit_name = models.CharField(max_length = 200)

    unit_number = models.PositiveIntegerField(blank=True, help_text="Do not change unless re-ordering units")
    
    class Meta:
        unique_together = (("course", "unit_name"), ("course", "unit_number"))

    def __str__(self):
        return self.course.course_name + " " + self.unit_name

    def generate_unit_order_number(self):
        last_unit = Unit.objects.filter(course=self.course).order_by('unit_number').last()
        if last_unit is not None:
            return last_unit.unit_number + 1
        else:
            return 1

    def save(self, *args, **kwargs):
        if not self.unit_number:
            self.unit_number = self.generate_unit_order_number()
        super().save(*args, **kwargs)

#======================================================
#Lesson
#======================================================
class Lesson(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    lesson_name = models.CharField(max_length = 200)

    lesson_number = models.PositiveIntegerField(blank=True, help_text="Do not change unless re-ordering lessons") 

    is_public = models.BooleanField(default=False)

    def random_id_generator():
        while True:
            lesson_id = get_random_string(6, '0123456789')
            if not Lesson.objects.filter(random_slug=lesson_id).exists():
                break
        return lesson_id

    random_slug = models.CharField(max_length = 6, unique=True, editable = False, default = random_id_generator)
    
    LESSON_TYPE_CHOICES = [
        ('VIDEO', 'Video'),
        ('QUIZ', 'Quiz'),
    ]

    lesson_type = models.CharField(max_length = 25, choices=LESSON_TYPE_CHOICES)

    #All possible formats of this lesson (choose exactly one and leave the rest blank):
    #--------------------------------
    video = models.ForeignKey('Video', blank=True, null=True, on_delete=models.PROTECT)
    #--------------------------------

    def __str__(self):
        return self.unit.course.course_name + " Unit " + str(self.unit.unit_number) + " " + self.lesson_name

    def get_next_lesson(self):
        """
        Checks to see if there are more lessons in the same unit.
        If yes, then get the info needed to render that lesson on the front end;
        if no, then return the next lesson type as 'NONE'
        """
        next_lesson_in_unit = Lesson.objects.filter(unit=self.unit, lesson_number__gt=self.lesson_number).order_by('lesson_number').first()
        
        if next_lesson_in_unit is not None:
            next_lesson_id = next_lesson_in_unit.random_slug
            next_lesson_type = next_lesson_in_unit.lesson_type

            if next_lesson_type == 'VIDEO' or next_lesson_type == 'QUIZ':
                return {'next_lesson_id':next_lesson_id, 'next_lesson_type':next_lesson_type}
            #else: add other lesson types in the future
              
        else:
            next_lesson_type = 'NONE'
            return {'next_lesson_type':next_lesson_type}

    def get_quiz_questions_context_json(self):
        quiz_questions = self.quiz_question_set.values_list('properties', flat=True)
        return list(quiz_questions)

    def generate_lesson_order_number(self):
        last_lesson = Lesson.objects.filter(unit=self.unit).order_by('lesson_number').last()
        if last_lesson is not None:
            return last_lesson.lesson_number + 1
        else:
            return 1
            
    def clean(self):
        """
        Make sure each lesson has exactly one lesson type.
        This is called by ModelForm when saving through ModelForm (e.g. Admin site).
        Be sure to call full_clean() if creating or updating by calling save().
        """
        if self.lesson_type == 'VIDEO' and not self.video:
            raise ValidationError('Lesson Type = video, but you are not pointing it to a video.')
        elif self.lesson_type == 'QUIZ' and self.video:
            raise ValidationError('Lesson Type = quiz, but you are pointing it to a video.')

    def save(self, *args, **kwargs):
        if not self.lesson_number:
            self.lesson_number = self.generate_lesson_order_number()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (("unit", "lesson_name"), ("unit", "lesson_number"))

#======================================================
#Video
#======================================================
class Video(models.Model):
    video_file_name = models.CharField(max_length = 200, default="")
    properties = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.video_file_name

    def get_video_questions_context_json(self):
        return self.properties


#======================================================
#Quiz_Question
#====================================================== 
class Quiz_Question(models.Model):
    lesson = models.ManyToManyField(Lesson)
    question_name = models.CharField(max_length = 200, help_text="This is what comes up in database search results. It does not appear in the actual quiz question.")
    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.question_name





