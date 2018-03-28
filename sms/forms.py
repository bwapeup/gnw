from django import forms
from django.contrib.auth.forms import UserCreationForm
from people.models import CustomUser


class SignUpForm(UserCreationForm):
    verification_code = forms.CharField(max_length=7, min_length=7)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'verification_code', )


class RequestSMSCodeForm(forms.Form):
    mobile = forms.CharField(label='Mobile Number', max_length=11, min_length=11)
    verification_code = forms.CharField(max_length=7, min_length=7)

    
