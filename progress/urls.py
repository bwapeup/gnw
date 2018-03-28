from django.conf.urls import url
from progress import views

urlpatterns = [
    url(r'^ajax/record_completed_lm/$', views.ajax_record_completed_lm, name='record_completed_lm'),
]



