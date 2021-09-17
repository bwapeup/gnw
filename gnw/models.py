from pathlib import Path
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

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

    random_slug = models.CharField(max_length = 6, unique=True, blank=True, help_text="Leave blank to use system default")

    LESSON_TYPE_CHOICES = [
        ('VIDEO', 'Video'),
        ('QUIZ', 'Quiz'),
        ('ASSIGNMENT', 'Assignment'),
    ]

    lesson_type = models.CharField(max_length = 25, choices=LESSON_TYPE_CHOICES)

    #All possible formats of this lesson (choose at most one and leave the rest blank):
    #--------------------------------
    video = models.ForeignKey('Video', blank=True, null=True, on_delete=models.PROTECT)
    assignment_details = models.JSONField(blank=True, null=True)
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

            if next_lesson_type in ['VIDEO', 'QUIZ', 'ASSIGNMENT']:
                return {'next_lesson_id':next_lesson_id, 'next_lesson_type':next_lesson_type}
            #else: add other lesson types in the future
              
        else:
            next_lesson_type = 'NONE'
            return {'next_lesson_type':next_lesson_type}

    def get_quiz_questions_context_json(self):
        quiz_questions = self.quiz_question_set.values_list('properties', flat=True)
        return list(quiz_questions)

    def get_assignment_details_json(self):
        return self.assignment_details
            
    def clean(self):
        """
        Make sure each lesson has exactly one lesson type.
        This is called by ModelForm when saving through ModelForm (e.g. Admin site).
        Be sure to call full_clean() if creating or updating by calling save().
        """
        if self.lesson_type == 'VIDEO' and not self.video:
            raise ValidationError('Lesson Type = video, but you are not pointing it to a video.')
        elif self.lesson_type == 'QUIZ' and (self.video or self.assignment_details):
            raise ValidationError('Lesson Type = quiz, but you provided details for a video or an assignment.')
        elif self.lesson_type == 'ASSIGNMENT' and not self.assignment_details:
            raise ValidationError('Lesson Type = assignment, but you left the assignment details blank.')

    def generate_lesson_order_number(self):
        last_lesson = Lesson.objects.filter(unit=self.unit).order_by('lesson_number').last()
        if last_lesson is not None:
            return last_lesson.lesson_number + 1
        else:
            return 1

    @classmethod
    def random_id_generator(cls):
        while True:
            lesson_id = get_random_string(6, '0123456789')
            if not cls.objects.filter(random_slug=lesson_id).exists():
                break
        return lesson_id

    def save(self, *args, **kwargs):
        if not self.lesson_number:
            self.lesson_number = self.generate_lesson_order_number()
        if not self.random_slug:
            self.random_slug = Lesson.random_id_generator()
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


#======================================================
#Assignment
#====================================================== 
class Assignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    submitted_time = models.DateTimeField(default=now, help_text="Leave blank to use system default") 

    graded = models.BooleanField(default=False)

    graded_time = models.DateTimeField(blank=True, null=True, help_text="Leave blank to use system default")

    properties = models.JSONField(blank=True, null=True, help_text="Leave blank for now")

    image1 = models.ImageField()
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)
    image6 = models.ImageField(blank=True, null=True)
    image7 = models.ImageField(blank=True, null=True)
    image8 = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return "Assignment for: " + self.lesson.lesson_name

    def get_assignment_context_json(self):
        return self.properties

    def get_assignment_context(self):
        """
        This is used in the JS frontend. If the model is restructured to
        use json only, this method will not be needed anymore.
        """
        ctx = {}
        ctx['submitted_time'] = self.submitted_time
        ctx['graded'] = self.graded
        ctx['graded_time'] = self.graded_time

        if self.graded:
            ctx['photos'] = []
            for i in range(1,9):
                image = getattr(self, 'image'+str(i))
                if image.name:
                    ctx['photos'].append(image.url)
        return ctx

    def assign_unique_names_to_images(self):
        """
        When an assignment is submitted, the uploaded images are renamed with 
        random characters so that no accidental override happens.
        """
        for i in range(1,9):
            image = getattr(self, 'image'+str(i))
            if image.name:
                file_extension = Path(image.name).suffix
                image.name = get_random_string(12) + file_extension

    def save(self, *args, **kwargs):
        if self.graded and not self.graded_time:
            self.graded_time = now()
        super().save(*args, **kwargs)
