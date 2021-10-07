from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from enrollment.models import Enrollment 
from gnw.models import Lesson


#Template Context Data
#----------------------------------------------------
def initialize_context(keys={'img_url'}):
    ctx_items = [
        ('img_url', 'gnw/img/'),
        ('video_url', 'gnw/video/'),
        ('audio_url', 'gnw/audio/'),
        ]
    ctx = {key: url for key, url in ctx_items if key in keys}
    return ctx


#Authorization and Permission
#-----------------------------------------------------
def user_allowed_to_access_course(request, slug):
    return is_enrolled(request, slug) or has_subscription(request, slug)  
    
def has_subscription(request, slug):
    return False

def is_enrolled(request, slug):
    return Enrollment.objects.filter(user=request.user, course__slug=slug, is_current=True).exists()


#Request Validity
#-----------------------------------------------------
def get_lesson_or_404(slug, uuid, type_check=None):
    try:
        if type_check == 'VIDEO':
            lesson = Lesson.objects.filter(random_slug=uuid).select_related('video', 'unit__course').get()
        else:
            lesson = Lesson.objects.filter(random_slug=uuid).select_related('unit__course').get()
    except ObjectDoesNotExist:
        raise Http404("Invalid lesson")

    if lesson.unit.course.slug != slug:
        raise Http404("Invalid lesson")

    if type_check:
        if lesson.lesson_type != type_check:
            raise Http404("Invalid lesson")

    return lesson