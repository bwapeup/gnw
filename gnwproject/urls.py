import debug_toolbar
from django.conf.urls import url, include
from django.contrib import admin
from gnw import views as gnw_views
from sms import views as sms_views
from people import views as people_views
from django.urls import path




urlpatterns = [
    url(r'^ycchtliaaau/', admin.site.urls, name='admin-page'),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^$', gnw_views.index, name='index'),
    url(r'^signup/$', sms_views.signup_captcha, name='signup'),
    url(r'^signup/activate/(?P<token>\w+)/$', sms_views.activate_new_user, name='activate_new_user'),
    url(r'^panel/$', gnw_views.panel, name='panel'),
    url(r'^panel/update_my_info/$', people_views.update_student_info, name='update_student_info'),
    url(r'^panel/show_my_info/$', people_views.show_my_info, name='show_my_info'),
    url(r'^my_courses/(?P<slug>[\w-]+)/$', gnw_views.course, name='class'),
    url(r'^my_courses/(?P<slug>[\w-]+)/video/(?P<uuid>\d+)/$', gnw_views.video, name='video'),
    url(r'^my_courses/(?P<slug>[\w-]+)/quiz/(?P<uuid>\d+)/$', gnw_views.quiz, name='quiz'),
]

#Ajax to request sms sign-up verification
urlpatterns += [
    url(r'^ajax/request_sms/(?P<token>\w+)/$', sms_views.ajax_send_sms_verification_code, name='ajax_send_sms_verification_code'),
]

#Request sms verification for password reset, etc. 
urlpatterns += [
    url(r'^reset_password_request/$', sms_views.reset_password_captcha, name='reset_password_captcha'),
    url(r'^reset_password_sms/(?P<token>\w+)/$', sms_views.reset_password_sms, name='reset_password_sms'),
    url(r'^reset_password_confirm/(?P<token>\w+)/$', sms_views.reset_password_confirm, name='reset_password_confirm'),
]

urlpatterns += [
    url(r'^progress/', include('progress.urls')),
]

urlpatterns += [
    url(r'^captcha/', include('captcha.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]







