from django.forms import ModelForm, SelectDateWidget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Student

BIRTH_YEAR_CHOICES=[str(i) for i in range(2020, 1999, -1)]

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class StudentInfoUpdateForm(ModelForm):
    
    class Meta:
        model = Student
        fields = ('parent_name', 'student_name', 'student_birth_date', 'student_gender', 'city')
        widgets = {
            'student_birth_date': SelectDateWidget(years=BIRTH_YEAR_CHOICES, empty_label=("年", "月", "日"),),
        }
