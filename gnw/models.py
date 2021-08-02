from django.utils.crypto import get_random_string
from django.db import models

#======================================================
#Course
#======================================================
class Course(models.Model):
    course_name = models.CharField(max_length = 200, unique=True)

    #Enter a URL-friendly name (using hyphens and underscores and no spaces) 
    #to be part of the URL:
    slug = models.SlugField(max_length = 200, unique=True)

    def __str__(self):
        return self.course_name

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

    def random_id_generator():
        id_not_generated = True
        while id_not_generated:
            lesson_id = get_random_string(6, '0123456789')
            if not Lesson.objects.filter(random_slug=lesson_id).exists():
                id_not_generated = False
        return lesson_id

    random_slug = models.CharField(max_length = 6, unique=True, editable = False, default = random_id_generator)
    
    LESSON_TYPE_CHOICES = [
        ('VIDEO', 'Video'),
        ('QUIZ', 'Quiz'),
    ]

    lesson_type = models.CharField(max_length = 25, choices=LESSON_TYPE_CHOICES)

    #All possible formats of this lesson:
    #To-do: Exactly one of the following must be non-null
    #--------------------------------
    video = models.ForeignKey('Video', blank=True, null=True, on_delete=models.PROTECT)
    quiz = models.ForeignKey('Quiz', blank=True, null=True, on_delete=models.PROTECT)
    #--------------------------------

    class Meta:
        unique_together = (("unit", "lesson_name"), ("unit", "lesson_number"))

    def __str__(self):
        return self.unit.course.course_name + " Unit " + str(self.unit.unit_number) + " " + self.lesson_name

    def get_next_lesson(self):
        #Checks to see if there are more lessons in the same unit.
        #If yes, then get the info needed to render that lesson on the front end;
        #if no, then return the next lesson type as 'NONE'
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

    def generate_lesson_order_number(self):
        last_lesson = Lesson.objects.filter(unit=self.unit).order_by('lesson_number').last()
        if last_lesson is not None:
            return last_lesson.lesson_number + 1
        else:
            return 1
            
    def save(self, *args, **kwargs):
        if not self.lesson_number:
            self.lesson_number = self.generate_lesson_order_number()
        super().save(*args, **kwargs)

#======================================================
#Video
#======================================================
class Video(models.Model):
    video_file_name = models.CharField(max_length = 200, default="")
    properties = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.video_file_name

    def get_video_questions_context(self):
        video_questions_dict = {}
        
        number_of_questions = 0
        video_questions = self.video_question_set.all()
        for question in video_questions:
            number_of_questions += 1
            video_questions_dict['question_' + str(number_of_questions)] = {}
            video_questions_dict['question_' + str(number_of_questions)]['pause_time'] = question.pause_time
            video_questions_dict['question_' + str(number_of_questions)]['resume_time'] = question.resume_time

            num_choices = question.number_of_choices
            video_questions_dict['question_' + str(number_of_questions)]['number_of_choices'] = num_choices
            video_questions_dict['question_' + str(number_of_questions)]['correct_choice'] = question.correct_choice

            video_is_branching = question.branching_video
            video_questions_dict['question_' + str(number_of_questions)]['branching_video'] = video_is_branching

            if video_is_branching:
                for i in range(1, num_choices + 1):
                    video_questions_dict['question_' + str(number_of_questions)]['start_time_branch_'+str(i)]=getattr(question, 'start_time_branch_'+str(i))
                    video_questions_dict['question_' + str(number_of_questions)]['end_time_branch_'+str(i)]=getattr(question, 'end_time_branch_'+str(i))

        return video_questions_dict

    
#======================================================
#Video_Question
#======================================================
class Video_Question(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    pause_time = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>")
    resume_time = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>")

    class Number_of_Choices(models.IntegerChoices):
        TWO = 2
        THREE = 3
        FOUR = 4

    number_of_choices = models.PositiveIntegerField(choices=Number_of_Choices.choices)

    class Choice(models.IntegerChoices):
        CHOICE_ONE = 1
        CHOICE_TWO = 2
        CHOICE_THREE = 3
        CHOICE_FOUR = 4

    correct_choice = models.PositiveIntegerField(choices=Choice.choices)

    branching_video  = models.BooleanField(default=False)

    start_time_branch_1 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)
    end_time_branch_1 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)

    start_time_branch_2 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)
    end_time_branch_2 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)

    start_time_branch_3 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)
    end_time_branch_3 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)

    start_time_branch_4 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)
    end_time_branch_4 = models.TimeField(help_text="format: <em>HH:MM:SS e.g. 00:01:29</em>", blank=True, null=True)

    def __str__(self):
        return self.video.video_file_name + ' ' + str(self.pause_time)

    #to-do:
    #(1). Check: correct_choice should be <= number_of_choices
    #(2). Check: if branching_video is True, then there should be a number of non-null
    #      branching times euqal to number_of_choices
    #(3). Conditional: Unless branching_video is set to be True, the branching times should
    #      not allow user input


#======================================================
#Quiz
#======================================================
class Quiz(models.Model):
    quiz_name = models.CharField(max_length = 200)
    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.quiz_name

    def get_quiz_questions_context(self):
        quiz_questions_dict = {}
        
        number_of_questions = 0
        quiz_questions = self.quiz_question_set.all()

        for question in quiz_questions:
            number_of_questions += 1
            quiz_questions_dict['question_' + str(number_of_questions)] = {}
            quiz_questions_dict['question_' + str(number_of_questions)]['question_title'] = question.question_title
            quiz_questions_dict['question_' + str(number_of_questions)]['type_of_options'] = question.type_of_options
            quiz_questions_dict['question_' + str(number_of_questions)]['media_file_type'] = question.media_file_type
            quiz_questions_dict['question_' + str(number_of_questions)]['media_file_name'] = question.media_file_name
            quiz_questions_dict['question_' + str(number_of_questions)]['correct_choice'] = question.correct_choice
 
            for i in range(1, 5):
                quiz_questions_dict['question_' + str(number_of_questions)]['option_'+str(i)]=getattr(question, 'option_'+str(i))
                
        return quiz_questions_dict

#======================================================
#Quiz_Question
#====================================================== 
class Quiz_Question(models.Model):
    quiz = models.ManyToManyField(Quiz)
    question_title = models.TextField(max_length=500)

    OPTION_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
    ]

    type_of_options = models.CharField(max_length=20, choices=OPTION_TYPE_CHOICES, default='TEXT')

    MEDIA_TYPE_CHOICES = [
        ('AUDIO', 'Audio'),
        ('IMAGE', 'Image'),
        ('NONE', 'None'),
    ]

    media_file_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='NONE')
    media_file_name = models.CharField(max_length=100, blank=True, null=True)

    class Choice(models.IntegerChoices):
        CHOICE_ONE = 1
        CHOICE_TWO = 2
        CHOICE_THREE = 3
        CHOICE_FOUR = 4

    correct_choice = models.PositiveIntegerField(choices=Choice.choices)

    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)

    def __str__(self):
        return self.question_title





