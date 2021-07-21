from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from gnw.models import Course, Lesson
from enrollment.models import Enrollment
from progress.models import Completed_Lessons

#Templates:
#--------------------------------------
index_template = 'gnw/index.html'
panel_template = 'gnw/panel.html'
course_template = 'gnw/course.html'
video_template = 'gnw/video.html'
#--------------------------------------

def index(request):
    return render(request, index_template)

@login_required
def panel(request):
    enrolled_classes = Enrollment.objects.filter(user=request.user, is_current=True).select_related('course')
    return render(request, panel_template, {'enrolled_classes':enrolled_classes})

@login_required 
def course(request, slug):
    #Check (1) whether the course requested exists, and (2) whether the user is enrolled in it
    if not Enrollment.objects.filter(user=request.user, course__slug=slug, is_current=True).exists():
        return redirect(reverse('panel'))
    
    #Below should not use first(). If there more than one course with the same slug, it should error out
    # so that it can be corrected.
    course = Course.objects.filter(slug=slug).prefetch_related('unit_set__lesson_set').first()

    #The block below is used to track completed lessons and enforce, if chosen to do so, 
    #learning sequence
    a = Completed_Lessons.objects
    b = a.filter(enrollment__user=request.user, enrollment__is_current=True, lesson__unit__course__slug=slug)
    clms = b.values_list('lesson__random_slug', flat=True)

    context = {'course':course, 'course_name':course.course_name, 'course_slug':slug, 'completed_LMs':clms}
    return render(request, course_template, context)
    
@login_required
def video(request, slug, uuid):
    if not Enrollment.objects.filter(user=request.user, course__slug=slug, is_current=True).exists():
        return redirect(reverse('panel'))

    lesson = get_object_or_404(Lesson, random_slug=uuid)

    if lesson.video is None:
        raise Http404("No video assigned to this lesson")
    else:
        video = lesson.video

    video_name = video.video_file_name
    course_slug = lesson.unit.course.slug

    next_lesson_dict = lesson.get_next_lesson()

    video_file_url = settings.VIDEO_URL + video_name
    js_url = settings.JS_URL
    img_url = settings.IMAGE_URL
    css_url = settings.CSS_URL

    context = {'video_file_url':video_file_url, 'js_url':js_url, 'img_url':img_url, 'css_url':css_url, 'course_slug':course_slug}
    context.update(next_lesson_dict)

    #Get interactive in-video question info:
    #(1). Get querySet for all Video_Question objects with foreign key on Video
    #(2). For each Video_Question, construct data structure to pass to JS
    #(3). Set up JS to implement each Video_Question

    video_questions_dict = video.get_video_questions_context()
    context['video_questions_dict'] = video_questions_dict
    return render(request, video_template, context)

