from django import forms
from django.contrib.auth.forms import UserCreationForm
from people.models import CustomUser
from captcha.fields import CaptchaField
import re


class CaptchaScreenForm(forms.Form):
    mobile = forms.CharField(max_length=11, min_length=11)
    captcha = CaptchaField()

    def clean_mobile(self):
        #This is the clean function for the 'mobile' field specifically
        #It does custom validation for the 'mobile' field
        mobile_number = self.cleaned_data['mobile']
        try:
            mobile_number_str = str(mobile_number)
        except ValueError:
            return mobile_number
        #Use regex to verify this is a China mobile number
        #(1): It starts with '1'
        #(2): It is consisted of all digits
        #(3): It has exactly 11 digits
        if re.match(r'^[1][0-9]{10}$', mobile_number_str):
            return mobile_number
        else:
            raise forms.ValidationError("请输入一个有效的手机号码")

    
class SignUpForm(UserCreationForm):
    """
    This form is not used currently. We are not allowing users to sign up on the website. 
    Users get signed up by us when they purchase our courses on the third-party ecommerce platform.
    """
    verification_code = forms.CharField(max_length=7, min_length=7)

    class Meta:
        model = CustomUser
        fields = ('username', 'mobile', 'password1', 'password2')


class RequestSMSCodeForm(forms.Form):
    verification_code = forms.CharField(max_length=6, min_length=6)

    
