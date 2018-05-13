from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db.models import F
from .models import SMS_Code, Token, Registration_Token
from people.models import Student
from django.contrib.auth.forms import SetPasswordForm
from .forms import SignUpForm, RequestSMSCodeForm, CaptchaScreenForm
from django.utils import timezone
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from django.conf import settings
from django.http import HttpResponse
from uuid import uuid4


User = get_user_model()
yunpian_apikey = getattr(settings, 'YUNPIAN_APIKEY', '')

def signup_captcha(request):
    if request.user.is_authenticated:
        return redirect(reverse('panel'))
    if request.method == 'POST':
        form = CaptchaScreenForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile')
            if User.objects.filter(username = mobile_number).exists():
                return render(request, 'sms/signup_captcha.html', {'form': form, 'mobile_already_registered':True})
            else:
                token_string = str(uuid4().hex)
                Registration_Token.objects.create(mobile=mobile_number, token_hex_str=token_string, created = timezone.now())
                return redirect(reverse('activate_new_user', kwargs={'token': token_string}))
        else:
            return render(request, 'sms/signup_captcha.html', {'form': form})
    else:
        form = CaptchaScreenForm()
        return render(request, 'sms/signup_captcha.html', {'form': form})


def activate_new_user(request, token):
    registration_token = Registration_Token.objects.filter(token_hex_str=token, verified=False, expired=False, sms_sent__lte=3).order_by('-created').first()
    if registration_token is None:
        return redirect(reverse('signup'))
    else:
        if (timezone.now() - registration_token.created).total_seconds() > 600: #Consider using F() and timedelta(seconds=xxx)
            return redirect(reverse('signup'))
    if request.method != 'POST':
        form = SignUpForm()
        return render(request, 'sms/activate_new_user.html', {'form': form, 'token_hex_str':token, 'mobile':registration_token.mobile})
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                hidden_mobile_field_tampered_with = str(registration_token.mobile).strip() != str(form.cleaned_data.get('username')).strip()
            except ValueError:
                return redirect(reverse('signup'))
            else:
                if hidden_mobile_field_tampered_with:
                    return redirect(reverse('signup'))
                
            sms = SMS_Code.objects.filter(mobile=registration_token.mobile, verified=False, expired=False, tries__lt=3).order_by('-created').first()
            if sms is None:
                context = {}
                context['form'] = form
                context['token_hex_str'] = token
                context['mobile'] = registration_token.mobile
                context['sms_authentication_failed'] = True
                return render(request, 'sms/activate_new_user.html', context)
            if sms.code != form.cleaned_data.get('verification_code'):
                sms.tries = F('tries') + 1
                sms.save()
                context = {}
                context['form'] = form
                context['token_hex_str'] = token
                context['mobile'] = registration_token.mobile
                context['sms_authentication_failed'] = True
                return render(request, 'sms/activate_new_user.html', context)
            if (timezone.now() - sms.created).total_seconds() > 90: #Consider using F() and timedelta(seconds=xxx)
                context = {}
                context['form'] = form
                context['token_hex_str'] = token
                context['mobile'] = registration_token.mobile
                context['sms_authentication_failed'] = True
                return render(request, 'sms/activate_new_user.html', context)
            if User.objects.filter(username = registration_token.mobile).exists():
                return redirect(reverse('signup'))
            else:
                form.save()
                raw_password = form.cleaned_data.get('password1')
                new_user = authenticate(username=registration_token.mobile, password=raw_password) 
                login(request, new_user)
                new_student = Student.objects.create(user=new_user, mobile=registration_token.mobile)
                sms.verified = True
                sms.save()
                registration_token.verified = True
                registration_token.save()
                return redirect(reverse('panel'))
        else:
            context = {}
            context['form'] = form
            context['token_hex_str'] = token
            context['mobile'] = registration_token.mobile
            return render(request, 'sms/activate_new_user.html', context)


def reset_password_captcha(request):
    if request.user.is_authenticated:
        return redirect(reverse('panel'))
    if request.method == 'POST':
        form = CaptchaScreenForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile')
            if not User.objects.filter(username = mobile_number).exists():
                return render(request, 'sms/reset_password_captcha.html', {'form': form})
            else:
                token_string = str(uuid4().hex)
                Registration_Token.objects.create(mobile=mobile_number, token_hex_str=token_string, created = timezone.now())
                return redirect(reverse('reset_password_sms', kwargs={'token': token_string}))
        else:
            return render(request, 'sms/reset_password_captcha.html', {'form': form})
    else:
        form = CaptchaScreenForm()
        return render(request, 'sms/reset_password_captcha.html', {'form': form})


def reset_password_sms(request, token):
    registration_token = Registration_Token.objects.filter(token_hex_str=token, verified=False, expired=False, sms_sent__lte=3).order_by('-created').first()
    if registration_token is None:
        return redirect(reverse('reset_password_captcha'))
    else:
        if (timezone.now() - registration_token.created).total_seconds() > 600: #Consider using F() and timedelta(seconds=xxx)
            return redirect(reverse('reset_password_captcha'))
    if request.method != 'POST':
        form = RequestSMSCodeForm()
        return render(request, 'sms/reset_password_sms.html', {'form': form, 'token_hex_str':token, 'mobile':registration_token.mobile})
    else:
        form = RequestSMSCodeForm(request.POST)
        if form.is_valid():                
            sms = SMS_Code.objects.filter(mobile=registration_token.mobile, verified=False, expired=False, tries__lt=3).order_by('-created').first()
            if sms is None:
                context = {}
                context['form'] = form
                context['token_hex_str'] = token
                context['mobile'] = registration_token.mobile
                context['sms_authentication_failed'] = True
                return render(request, 'sms/reset_password_sms.html', context)
            if (timezone.now() - sms.created).total_seconds() > 90: #Consider using F() and timedelta(seconds=xxx)
                context = {}
                context['form'] = form
                context['token_hex_str'] = token
                context['mobile'] = registration_token.mobile
                context['sms_authentication_failed'] = True
                return render(request, 'sms/reset_password_sms.html', context)
            if sms.code != form.cleaned_data.get('verification_code'):
                sms.tries = F('tries') + 1
                sms.save()
                context = {}
                context['form'] = form
                context['token_hex_str'] = token
                context['mobile'] = registration_token.mobile
                context['sms_authentication_failed'] = True
                return render(request, 'sms/reset_password_sms.html', context)
            current_user = User.objects.filter(username = registration_token.mobile).first()
            if current_user is None:
                return redirect(reverse('reset_password_captcha')) #This should never happen
            sms.verified = True
            sms.save()
            registration_token.verified = True
            registration_token.save()
            token_string = str(uuid4().hex)
            login(request, current_user)
            Token.objects.create(mobile=registration_token.mobile, session_key=request.session.session_key, token_hex_str=token_string, created = timezone.now())
            return redirect(reverse('reset_password_confirm', kwargs={'token': token_string}))
        else:
            context = {}
            context['form'] = form
            context['token_hex_str'] = token
            context['mobile'] = registration_token.mobile
            return render(request, 'sms/reset_password_sms.html', context)


def reset_password_confirm(request, token):
    if not request.user.is_authenticated:
        return redirect(reverse('reset_password_captcha'))
    change_psswd_token = Token.objects.filter(mobile=request.user.username, session_key=request.session.session_key, token_hex_str=token, verified=False, expired=False).first()
    if change_psswd_token is None:
        return redirect(reverse('reset_password_captcha'))
    if request.method != 'POST':
        form = SetPasswordForm(request.user)
        return render(request, 'sms/reset_password.html', {'form': form, 'token_hex_str':token})
    else:
        if (timezone.now() - change_psswd_token.created).total_seconds() > 600: #Consider using F() and timedelta(seconds=600)
            return redirect(reverse('reset_password_captcha'))
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            change_psswd_token.verified = True
            change_psswd_token.save()
            update_session_auth_hash(request, request.user)
            return redirect(reverse('panel'))
        else:
            return render(request, 'sms/reset_password.html', {'form': form, 'token_hex_str':token, 'password_change_failed': True})


def ajax_send_sms_verification_code(request, token):
    if request.method == 'POST':
        registration_token = Registration_Token.objects.filter(token_hex_str=token, verified=False, expired=False, sms_sent__lte=3).order_by('-created').first()
        if registration_token is None:
            return HttpResponse(status=404)
        
        #check if a code has been sent to the user less than 1.5 minutes ago.
        sms_request = SMS_Code.objects.filter(mobile=registration_token.mobile, verified=False, expired=False).order_by('-created').first()
        if sms_request is None:
            verification_code = '1234567' #User.objects.make_random_password(length=7, allowed_chars='1234567890')
            
            #clnt = YunpianClient(yunpian_apikey)
            #param = {YC.MOBILE:mobile_number,YC.TEXT:'【云片网】您的验证码是'+verification_code}
            #r = clnt.sms().single_send(param)
            SMS_Code.objects.create(mobile=registration_token.mobile, code=verification_code, created = timezone.now())
            registration_token.sms_sent = F('sms_sent') + 1
            registration_token.save()
            
            return HttpResponse("sms sent")
        else:
            if (timezone.now() - sms_request.created).total_seconds() > 90: #Consider using F() and timedelta(seconds=xxx)
                verification_code = '1234567' #User.objects.make_random_password(length=7, allowed_chars='1234567890')
                
                #clnt = YunpianClient(yunpian_apikey)
                #param = {YC.MOBILE:mobile_number,YC.TEXT:'【云片网】您的验证码是'+verification_code}
                #r = clnt.sms().single_send(param)

                SMS_Code.objects.create(mobile=registration_token.mobile, code=verification_code, created = timezone.now())
                registration_token.sms_sent = F('sms_sent') + 1
                registration_token.save()
    
                return HttpResponse("sms sent")
            
            else:
                return HttpResponse("last sms sent within the last 90 seconds")

    else:
        return HttpResponse(status=405)

