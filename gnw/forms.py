from django.forms import ModelForm, CharField
from gnw.models import Assignment

class Submitted_Assignment_Form(ModelForm):

    lesson_uuid = CharField(max_length=6, min_length=6)
    course_slug = CharField(max_length=200)

    class Meta:
        model = Assignment
        fields = [
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'image6',
            'image7',
            'image8'
            ]