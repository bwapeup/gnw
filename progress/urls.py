from django.conf.urls import url
from progress import views

urlpatterns = [
    url(r'^ajax/record_completed_lesson/$', views.ajax_record_completed_lesson, name='record_completed_lesson'),
]



