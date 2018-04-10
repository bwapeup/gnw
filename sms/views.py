from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from .models import SMS_Code, Token
from people.models import Student
from django.contrib.auth.forms import SetPasswordForm
from .forms import SignUpForm, RequestSMSCodeForm
from django.utils import timezone
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from django.conf import settings
from django.http import HttpResponse
from uuid import uuid4

User = get_user_model()
yunpian_apikey = getattr(settings, 'YUNPIAN_APIKEY', '')

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('panel'))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('username')
            sms_request = SMS_Code.objects.filter(mobile=mobile_number, verified=False, expired=False).order_by('-created').first()
            if sms_request is None:
                return render(request, 'sms/signup.html', {'form': form, 'sms_authentication_failed': True})
            else:
                if (timezone.now() - sms_request.created).total_seconds() > 180: #Consider using F() and timedelta(seconds=180)
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
                        sms_request.verified = True
                        sms_request.save()
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
                sms_request = SMS_Code.objects.filter(mobile=mobile_number, verified=False, expired=False).order_by('-created').first()
                if sms_request is None:
                    return render(request, 'sms/sms_request.html', {'form': form, 'sms_authentication_failed': True})
                else:
                    if (timezone.now() - sms_request.created).total_seconds() > 30: #Consider using F() and timedelta(seconds=30)
                        return render(request, 'sms/sms_request.html', {'form': form, 'sms_authentication_failed': True})
                    else:
                        if sms_request.code != form.cleaned_data.get('verification_code'):
                            return render(request, 'sms/sms_request.html', {'form': form, 'sms_authentication_failed': True})
                        else:
                            sms_request.verified = True
                            sms_request.save()
                            token_string = str(uuid4().hex)
                            login(request, current_user)
                            Token.objects.create(mobile=mobile_number, session_key=request.session.session_key, token_hex_str=token_string, created = timezone.now())
                            return redirect(reverse('reset_password', kwargs={'token': token_string}))
            else:
                return render(request, 'sms/sms_request.html', {'form': form})
        else:
            return render(request, 'sms/sms_request.html', {'form': form})
    else:
        form = RequestSMSCodeForm()
        return render(request, 'sms/sms_request.html', {'form': form})


def reset_password(request, token):
    if not request.user.is_authenticated:
        return redirect(reverse('request_sms_code'))
    change_psswd_token = Token.objects.filter(mobile=request.user.username, session_key=request.session.session_key, token_hex_str=token, verified=False, expired=False).first()
    if change_psswd_token is None:
        return redirect(reverse('request_sms_code'))
    if request.method != 'POST':
        form = SetPasswordForm(request.user)
        return render(request, 'sms/reset_password.html', {'form': form, 'token_hex_str':token})
    else:
        if (timezone.now() - change_psswd_token.created).total_seconds() > 600: #Consider using F() and timedelta(seconds=600)
            return redirect(reverse('request_sms_code'))
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            change_psswd_token.verified = True
            change_psswd_token.save()
            update_session_auth_hash(request, request.user)
            return redirect(reverse('panel'))
        else:
            return render(request, 'sms/reset_password.html', {'form': form, 'sms_authentication_failed': True})
            


def ajax_send_sms_verification_code(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile')

        #check if a code has been sent to the user less than 3 minutes ago.
        sms_request = SMS_Code.objects.filter(mobile=mobile_number, verified=False, expired=False).order_by('-created').first()
        if sms_request is None:
            verification_code = '1234567' #User.objects.make_random_password(length=7, allowed_chars='1234567890')
            
            #clnt = YunpianClient(yunpian_apikey)
            #param = {YC.MOBILE:mobile_number,YC.TEXT:'【云片网】您的验证码是'+verification_code}
            #r = clnt.sms().single_send(param)
            SMS_Code.objects.create(mobile=mobile_number, code=verification_code, created = timezone.now())
            
            return HttpResponse("sms sent")
        else:
            if (timezone.now() - sms_request.created).total_seconds() > 0: #Consider using F() and timedelta(seconds=180)
                verification_code = '1234567' #User.objects.make_random_password(length=7, allowed_chars='1234567890')
                SMS_Code.objects.create(mobile=mobile_number, code=verification_code, created = timezone.now())
                
                #clnt = YunpianClient(yunpian_apikey)
                #param = {YC.MOBILE:mobile_number,YC.TEXT:'【云片网】您的验证码是'+verification_code}
                #r = clnt.sms().single_send(param)
    
                return HttpResponse("sms sent")
            
            else:
                return HttpResponse("too many sms requests")

    else:
        return HttpResponse("")
