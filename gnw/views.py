from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from gnw.models import Course, Lesson
from enrollment.models import Enrollment
from progress.models import Completed_Lessons


#Templates:
#--------------------------------------
index_template = 'gnw/index.html'
panel_template = 'gnw/panel.html'
course_template = 'gnw/course.html'
video_template = 'gnw/video.html'
quiz_template = 'gnw/quiz.html'
#--------------------------------------

#Context Data
#----------------------------------------------------------
def initialize_context(keys={'img_url'}):
    ctx_items = [
        ('img_url', 'gnw/assets/img/'),
        ('video_url', 'gnw/assets/video/'),
        ('audio_url', 'gnw/assets/audio/'),
        ]
    ctx = {key: url for key, url in ctx_items if key in keys}
    return ctx
#----------------------------------------------------------


def index(request):
    template_context = initialize_context() 
    return render(request, index_template, template_context)

@login_required
def panel(request):
    enrolled_classes = Enrollment.objects.filter(user=request.user, is_current=True).select_related('course')
    template_context = initialize_context()
    template_context.update({'enrolled_classes':enrolled_classes})
    return render(request, panel_template, template_context)

@login_required 
def course(request, slug):
    if not user_allowed_to_access_course(request, slug):
        return redirect(reverse('panel'))
    
    course = Course.objects.filter(slug=slug).prefetch_related('unit_set__lesson_set').first()

    #The block below is used to track completed lessons and enforce, if chosen to do so, 
    #learning sequence
    a = Completed_Lessons.objects
    b = a.filter(enrollment__user=request.user, enrollment__is_current=True, enrollment__course=course)
    cls = b.values_list('lesson__random_slug', flat=True)

    template_context = initialize_context()
    template_context.update({'course':course, 'course_name':course.course_name, 'course_slug':slug, 
               'completed_Lessons':cls}) 
    return render(request, course_template, template_context)
    
@login_required
def video(request, slug, uuid):
    if not user_allowed_to_access_course(request, slug):
        return redirect(reverse('panel'))

    try:
        lesson = Lesson.objects.filter(random_slug=uuid).select_related('video', 'unit__course').get()
    except ObjectDoesNotExist:
        raise Http404("This lesson does not exist")

    if lesson.unit.course.slug != slug:
        raise Http404("This lesson does not exist")

    if lesson.video is None:
        raise Http404("No video assigned to this lesson")
    else:
        video = lesson.video

    video_name = video.video_file_name
    course_slug = slug

    next_lesson_dict = lesson.get_next_lesson()

    template_context = initialize_context({'img_url', 'video_url'})
    template_context.update(next_lesson_dict)

    template_context.update({'video_name':video_name, 'course_slug':course_slug, 'lesson_id':uuid}) 

    video_questions_list = video.get_video_questions_context_json()
    template_context['video_questions_list'] = video_questions_list
    return render(request, video_template, template_context)

@login_required
def quiz(request, slug, uuid):
    if not user_allowed_to_access_course(request, slug):
        return redirect(reverse('panel'))

    try:
        lesson = Lesson.objects.filter(random_slug=uuid).select_related('unit__course').get()
    except ObjectDoesNotExist:
        raise Http404("This lesson does not exist")

    if lesson.unit.course.slug != slug:
        raise Http404("This lesson does not exist")

    course_slug = slug
    next_lesson_dict = lesson.get_next_lesson()

    template_context = initialize_context({'img_url', 'audio_url'})
    template_context.update(next_lesson_dict)

    template_context.update({'course_slug':course_slug, 'lesson_id':uuid}) 

    quiz_questions_list = lesson.get_quiz_questions_context_json()
    template_context['quiz_questions_list'] = quiz_questions_list
    return render(request, quiz_template, template_context)

        
def user_allowed_to_access_course(request, slug):
    return is_enrolled(request, slug) or has_subscription(request, slug)  
    
def has_subscription(request, slug):
    return False

def is_enrolled(request, slug):
    return Enrollment.objects.filter(user=request.user, course__slug=slug, is_current=True).exists()