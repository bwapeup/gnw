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
    unit_number = models.PositiveIntegerField() #to-do: On new create, it should be assigned automatically
    
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
    lesson_number = models.PositiveIntegerField() #to-do: On new create, it should be assigned automatically
    random_slug = models.CharField(max_length = 6, unique=True) #to-do: On new create, it should be assigned automatically
    
    LESSON_TYPE_CHOICES = [
        ('VIDEO', 'Video'),
        ('QUIZ', 'Quiz'),
    ]

    lesson_type = models.CharField(max_length = 25, choices=LESSON_TYPE_CHOICES)

    #All possible formats of this lesson:
    #To-do: Exactly one of the following must be non-null
    #--------------------------------
    video = models.ForeignKey('Video', blank=True, null=True, on_delete=models.PROTECT)
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

            if next_lesson_type == 'VIDEO':
                return {'next_lesson_id':next_lesson_id, 'next_lesson_type':next_lesson_type}
            #elif: Add other lesson types

        else:
            next_lesson_type = 'NONE'
            return {'next_lesson_type':next_lesson_type}

#======================================================
#Video
#======================================================
class Video(models.Model):
    video_file_name = models.CharField(max_length = 200, default="")
    
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
#Interactive In-Video Question
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