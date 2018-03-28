"""gnw1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from gnw import views as gnw_views
from sms import views as sms_views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin-page'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^$', gnw_views.index, name='index'),
    url(r'^signup/$', sms_views.signup, name='signup'),
    url(r'^panel/$', gnw_views.panel, name='panel'),
    url(r'^panel/my_courses/(?P<slug>\w+)/$', gnw_views.course, name='class'),
    url(r'^panel/my_courses/(?P<slug>\w+)/lecture/(?P<uuid>\d+)/$', gnw_views.lecture, name='VD'),
]

#The main courses page listing all the courses available with links to each individual course
urlpatterns += [
    url(r'^courses/$', gnw_views.courses_main_page, name='courses_main_page'),
]

#Ajax to request sms sign-up verification
urlpatterns += [
    url(r'^ajax/request_sms/$', sms_views.ajax_send_sms_verification_code, name='ajax_send_sms_verification_code'),
]

#Request sms verification for password reset, etc. 
urlpatterns += [
    url(r'^sms_request/$', sms_views.request_sms_code, name='request_sms_code'),
    url(r'^sms_password_change/$', sms_views.reset_password, name='reset_password'),
]

urlpatterns += [
    url(r'^progress/', include('progress.urls')),
]







