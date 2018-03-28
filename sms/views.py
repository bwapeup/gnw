from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from .models import SMS_Code
from people.models import Student
from django.contrib.auth.forms import SetPasswordForm
from .forms import SignUpForm, RequestSMSCodeForm
from django.utils import timezone
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from django.conf import settings
from django.http import HttpResponse

User = get_user_model()
yunpian_apikey = getattr(settings, 'YUNPIAN_APIKEY', '')

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('panel'))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('username')
            if not SMS_Code.objects.filter(mobile=mobile_number).exists():
                return render(request, 'sms/signup.html', {'form': form, 'sms_authentication_failed': True})
            else:
                sms_request = SMS_Code.objects.filter(mobile=mobile_number).first()
                if (timezone.now() - sms_request.last_update).total_seconds() > 180: #Consider using F() and timedelta(seconds=180)
                    return render(request, 'sms/signup.html', {'form': form, 'sms_authentication_failed': True})
                else:
                    if sms_request.code != form.cleaned_data.get('verification_code'):
                        return render(request, 'sms/signup.html', {'form': form, 'sms_authentication_failed': True})
                    else:
                        form.save()
                        raw_password = form.cleaned_data.get('password1')
                        new_user = authenticate(username=mobile_number, password=raw_password) 
                        login(request, new_user)
                        new_student = Student.objects.create(user=new_user, mobile=mobile_number)
                        sms_request.delete()
                        return redirect(reverse('panel'))
        else:
            return render(request, 'sms/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'sms/signup.html', {'form': form})


def request_sms_code(request):
    if request.user.is_authenticated:
        return redirect(reverse('panel'))
    if request.method == 'POST':
        form = RequestSMSCodeForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile')
            current_user = User.objects.filter(username=mobile_number).first()
            if current_user is not None:
                sms_request = SMS_Code.objects.filter(mobile=mobile_number).first()
                if sms_request is None:
                    return render(request, 'sms/sms_request.html', {'form': form, 'sms_authentication_failed': True})
                else:
                    if (timezone.now() - sms_request.last_update).total_seconds() > 30: #Consider using F() and timedelta(seconds=30)
                        return render(request, 'sms/sms_request.html', {'form': form, 'sms_authentication_failed': True})
                    else:
                        if sms_request.code != form.cleaned_data.get('verification_code'):
                            return render(request, 'sms/sms_request.html', {'form': form, 'sms_authentication_failed': True})
                        else:
                            sms_request.verified = True
                            sms_request.save()
                            login(request, current_user)
                            return redirect(reverse('reset_password'))
            else:
                return render(request, 'sms/sms_request.html', {'form': form})
        else:
            return render(request, 'sms/sms_request.html', {'form': form})
    else:
        form = RequestSMSCodeForm()
        return render(request, 'sms/sms_request.html', {'form': form})


def reset_password(request):
    if not request.user.is_authenticated:
        return redirect(reverse('request_sms_code'))
    sms_request = SMS_Code.objects.filter(mobile=request.user.username).first()
    if sms_request is None:
        return redirect(reverse('request_sms_code'))
    if request.method != 'POST':
        form = SetPasswordForm(request.user)
        return render(request, 'sms/reset_password.html', {'form': form})
    else:
        if (timezone.now() - sms_request.last_update).total_seconds() > 600: #Consider using F() and timedelta(seconds=600)
            return redirect(reverse('request_sms_code'))
        if sms_request.verified != True:
            return redirect(reverse('request_sms_code'))
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect(reverse('panel'))
        else:
            return render(request, 'sms/reset_password.html', {'form': form, 'sms_authentication_failed': True})
            


def ajax_send_sms_verification_code(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile')

        #check if a code has been sent to the user less than 3 minutes ago.
        sms_request = SMS_Code.objects.filter(mobile=mobile_number).first()
        if sms_request is None:
            verification_code = '1234567' #User.objects.make_random_password(length=6, allowed_chars='1234567890')
            
            #clnt = YunpianClient(yunpian_apikey)
            #param = {YC.MOBILE:mobile_number,YC.TEXT:'【云片网】您的验证码是'+verification_code}
            #r = clnt.sms().single_send(param)
            sms_request = SMS_Code.objects.create(mobile=mobile_number, code=verification_code, last_update = timezone.now())
            
            return HttpResponse("sms sent")
        else:
            if (timezone.now() - sms_request.last_update).total_seconds() > 180: #Consider using F() and timedelta(seconds=180)
                verification_code = '1234567' #User.objects.make_random_password(length=6, allowed_chars='1234567890')
                sms_request.code = verification_code
                
                #clnt = YunpianClient(yunpian_apikey)
                #param = {YC.MOBILE:mobile_number,YC.TEXT:'【云片网】您的验证码是'+verification_code}
                #r = clnt.sms().single_send(param)
                sms_request.last_update = timezone.now()
                sms_request.save()
            
                return HttpResponse("sms sent")
            
            else:
                return HttpResponse("too many sms requests")

    else:
        return redirect(reverse('index'))
