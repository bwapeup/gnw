from uuid import uuid4
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
#from django.core.mail import mail_managers
from django.db.models import F
from .models import SMS_Code, Token, Registration_Token
from .forms import SignUpForm, RequestSMSCodeForm, CaptchaScreenForm
from .helpers import send_sms



User = get_user_model()

#Templates:
#--------------------------------------
signup_captcha_template = 'sms/signup_captcha.html'
activate_new_user_template = 'sms/activate_new_user.html'
reset_password_captcha_template = 'sms/reset_password_captcha.html'
reset_password_sms_template = 'sms/reset_password_sms.html'
reset_password_template = 'sms/reset_password.html'
require_password_change_template = 'sms/require_password_change.html'
#--------------------------------------

template_context = {}

def signup_captcha(request):
    """
    This function is not used currently. The url that routes to this view function is disabled, as 
    we are not allowing users to sign up on the website. Users get signed up by us when they purchase
    our courses on the third-party ecommerce platform.
    """
    if request.user.is_authenticated:
        return redirect(reverse('panel'))
    if request.method == 'POST':
        form = CaptchaScreenForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile')
            if User.objects.filter(mobile = mobile_number).exists():
                template_context.update({'form': form, 'mobile_already_registered':True})
                return render(request, signup_captcha_template, template_context)
            else:
                token_string = str(uuid4().hex)
                Registration_Token.objects.create(mobile=mobile_number, token_hex_str=token_string, created = timezone.now())
                return redirect(reverse('activate_new_user', kwargs={'token': token_string}))
        else:
            template_context.update({'form': form})
            return render(request, signup_captcha_template, template_context)
    else:
        form = CaptchaScreenForm()
        template_context.update({'form': form})
        return render(request, signup_captcha_template, template_context)


def activate_new_user(request, token):
    """
    This function is not used currently. The url that routes to this view function is disabled, as 
    we are not allowing users to sign up on the website. Users get signed up by us when they purchase
    our courses on the third-party ecommerce platform.
    """
    registration_token = Registration_Token.objects.filter(token_hex_str=token, verified=False, expired=False, sms_sent__lte=3).order_by('-created').first()
    if registration_token is None:
        return redirect(reverse('signup'))
    else:
        if (timezone.now() - registration_token.created).total_seconds() > 600: #Consider using F() and timedelta(seconds=xxx)
            return redirect(reverse('signup'))
    if request.method != 'POST':
        form = SignUpForm()
        template_context.update({'form': form, 'token_hex_str':token, 'mobile':registration_token.mobile})
        return render(request, activate_new_user_template, template_context)
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                hidden_mobile_field_tampered_with = str(registration_token.mobile).strip() != str(form.cleaned_data.get('mobile')).strip()
            except ValueError:
                return redirect(reverse('signup'))
            else:
                if hidden_mobile_field_tampered_with:
                    return redirect(reverse('signup'))
                
            sms = SMS_Code.objects.filter(mobile=registration_token.mobile, verified=False, expired=False, tries__lt=3).order_by('-created').first()
            if sms is None:
                template_context['form'] = form
                template_context['token_hex_str'] = token
                template_context['mobile'] = registration_token.mobile
                template_context['sms_authentication_failed'] = True
                return render(request, activate_new_user_template, template_context)
            if sms.code != form.cleaned_data.get('verification_code'):
                sms.tries = F('tries') + 1
                sms.save()
                template_context['form'] = form
                template_context['token_hex_str'] = token
                template_context['mobile'] = registration_token.mobile
                template_context['sms_authentication_failed'] = True
                return render(request, activate_new_user_template, template_context)
            if (timezone.now() - sms.created).total_seconds() > 90: #Consider using F() and timedelta(seconds=xxx)
                template_context['form'] = form
                template_context['token_hex_str'] = token
                template_context['mobile'] = registration_token.mobile
                template_context['sms_authentication_failed'] = True
                return render(request, activate_new_user_template, template_context)
            #if User.objects.filter(username = registration_token.mobile).exists():
                #return redirect(reverse('signup'))
            else:
                form.save()
                raw_password = form.cleaned_data.get('password1')
                username = form.cleaned_data.get('username')
                new_user = authenticate(username=username, password=raw_password) 
                if new_user is not None:
                    login(request, new_user)
                else:
                    return redirect(reverse('signup'))
                sms.verified = True
                sms.save()
                registration_token.verified = True
                registration_token.save()
                messages.success(request, '欢迎加入飞猫星球!')
                #mail_managers(
                #    'New User Registration; ' + 'Time: ' + str(timezone.now()),
                #    'User mobile: ' + str(registration_token.mobile),
                #)
                return redirect(reverse('panel'))
        else:
            template_context['form'] = form
            template_context['token_hex_str'] = token
            template_context['mobile'] = registration_token.mobile
            return render(request, activate_new_user_template, template_context)


def reset_password_captcha(request):
    if request.user.is_authenticated:
        return redirect(reverse('panel'))
    if request.method == 'POST':
        form = CaptchaScreenForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data.get('mobile')
            #Is below the best option to avoid leaking information?
            if not User.objects.filter(mobile = mobile_number).exists():
                template_context.update({'form': form})
                return render(request, reset_password_captcha_template, template_context)
            else:
                token_string = str(uuid4().hex)
                Registration_Token.objects.create(mobile=mobile_number, token_hex_str=token_string, created = timezone.now())
                return redirect(reverse('reset_password_sms', kwargs={'token': token_string}))
        else:
            template_context.update({'form': form})
            return render(request, reset_password_captcha_template, template_context)
    else:
        form = CaptchaScreenForm()
        template_context.update({'form': form})
        return render(request, reset_password_captcha_template, template_context)


def reset_password_sms(request, token):
    registration_token = Registration_Token.objects.filter(token_hex_str=token, verified=False, expired=False, sms_sent__lte=3).order_by('-created').first()
    if registration_token is None:
        return redirect(reverse('reset_password_captcha'))
    else:
        if (timezone.now() - registration_token.created).total_seconds() > 600: #Consider using F() and timedelta(seconds=xxx)
            return redirect(reverse('reset_password_captcha'))
    if request.method != 'POST':
        form = RequestSMSCodeForm()
        template_context.update({'form': form, 'token_hex_str':token, 'mobile':registration_token.mobile})
        return render(request, reset_password_sms_template, template_context)
    else:
        form = RequestSMSCodeForm(request.POST)
        if form.is_valid():                
            sms = SMS_Code.objects.filter(mobile=registration_token.mobile, verified=False, expired=False, tries__lt=3).order_by('-created').first()
            if sms is None:
                template_context['form'] = form
                template_context['token_hex_str'] = token
                template_context['mobile'] = registration_token.mobile
                template_context['sms_authentication_failed'] = True
                return render(request, reset_password_sms_template, template_context)
            if (timezone.now() - sms.created).total_seconds() > 90: #Consider using F() and timedelta(seconds=xxx)
                template_context['form'] = form
                template_context['token_hex_str'] = token
                template_context['mobile'] = registration_token.mobile
                template_context['sms_authentication_failed'] = True
                return render(request, reset_password_sms_template, template_context)
            if sms.code != form.cleaned_data.get('verification_code'):
                sms.tries = F('tries') + 1
                sms.save()
                template_context['form'] = form
                template_context['token_hex_str'] = token
                template_context['mobile'] = registration_token.mobile
                template_context['sms_authentication_failed'] = True
                return render(request, reset_password_sms_template, template_context)
            current_user = User.objects.filter(mobile = registration_token.mobile).first()
            if current_user is None:
                return redirect(reverse('reset_password_captcha')) #This should never happen
            sms.verified = True
            sms.save()
            registration_token.verified = True
            registration_token.save()
            token_string = str(uuid4().hex)
            login(request, current_user, backend='people.backends.MobileBackend')
            Token.objects.create(mobile=registration_token.mobile, session_key=request.session.session_key, token_hex_str=token_string, created = timezone.now())
            return redirect(reverse('reset_password_confirm', kwargs={'token': token_string}))
        else:
            template_context['form'] = form
            template_context['token_hex_str'] = token
            template_context['mobile'] = registration_token.mobile
            return render(request, reset_password_sms_template, template_context)

def reset_password_confirm(request, token):
    if not request.user.is_authenticated:
        return redirect(reverse('reset_password_captcha'))
    change_psswd_token = Token.objects.filter(mobile=request.user.mobile, session_key=request.session.session_key, token_hex_str=token, verified=False, expired=False).first()
    if change_psswd_token is None:
        return redirect(reverse('reset_password_captcha'))
    if request.method != 'POST':
        form = SetPasswordForm(request.user)
        template_context.update({'form': form, 'token_hex_str':token})
        return render(request, reset_password_template, template_context)
    else:
        if (timezone.now() - change_psswd_token.created).total_seconds() > 600: #Consider using F() and timedelta(seconds=600)
            return redirect(reverse('reset_password_captcha'))
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            change_psswd_token.verified = True
            change_psswd_token.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, '密码更改成功。下次登陆请记住输入新密码。')
            return redirect(reverse('panel'))
        else:
            template_context.update({'form': form, 'token_hex_str':token, 'password_change_failed': True})
            return render(request, reset_password_template, template_context)

@login_required 
def require_password_change(request):
    if request.method != 'POST':
        form = SetPasswordForm(request.user)
        template_context.update({'form': form})
        return render(request, require_password_change_template, template_context)
    else:
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            user = request.user
            user.require_password_change = False
            user.save(update_fields=['require_password_change'])
            update_session_auth_hash(request, user)
            messages.success(request, '密码更改成功。下次登陆请记住输入新密码。')
            return redirect(reverse('panel'))
        else:
            template_context.update({'form': form, 'password_change_failed': True})
            return render(request, require_password_change_template, template_context)

@require_POST
def ajax_send_sms_verification_code(request, token):
    registration_token = Registration_Token.objects.filter(token_hex_str=token, verified=False, expired=False, sms_sent__lte=3).order_by('-created').first()
    if registration_token is None:
        return HttpResponse(status=401)
    
    #check if a code has been sent to the user less than 1.5 minutes ago.
    sms_request = SMS_Code.objects.filter(mobile=registration_token.mobile, verified=False, expired=False).order_by('-created').first()
    if sms_request is None:
        verification_code = '123456' 
        #verification_code = get_random_string(6, '0123456789')
        send_sms(registration_token.mobile, verification_code)
        
        SMS_Code.objects.create(mobile=registration_token.mobile, code=verification_code, created = timezone.now())
        registration_token.sms_sent = F('sms_sent') + 1
        registration_token.save()
        
        return HttpResponse("sms sent")
    else:
        if (timezone.now() - sms_request.created).total_seconds() > 90: #Consider using F() and timedelta(seconds=xxx)
            verification_code = '123456' 
            #verification_code = get_random_string(6, '0123456789')
            send_sms(registration_token.mobile, verification_code)

            SMS_Code.objects.create(mobile=registration_token.mobile, code=verification_code, created = timezone.now())
            registration_token.sms_sent = F('sms_sent') + 1
            registration_token.save()

            return HttpResponse("sms sent")
        
        else:
            return HttpResponse(status=403)


