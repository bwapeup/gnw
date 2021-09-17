from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from enrollment.models import Enrollment
from progress.models import Completed_Lessons
from progress.views import create_completed_lesson_record
from gnw.models import Course, Assignment
from gnw.helpers import user_allowed_to_access_course, get_lesson_or_404, initialize_context
from gnw.forms import Submitted_Assignment_Form

#Templates:
#--------------------------------------
index_template = 'gnw/index.html'
panel_template = 'gnw/panel.html'
course_template = 'gnw/course.html'
video_template = 'gnw/video.html'
quiz_template = 'gnw/quiz.html'
assignment_template = 'gnw/assignment.html'
#--------------------------------------


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

    lesson = get_lesson_or_404(slug, uuid, 'VIDEO')

    if lesson.video is None:
        raise Http404("No video assigned to this lesson")
    else:
        video = lesson.video

    video_name = video.video_file_name

    next_lesson_dict = lesson.get_next_lesson()

    template_context = initialize_context({'img_url', 'video_url'})
    template_context.update(next_lesson_dict)

    template_context.update({'video_name':video_name, 'course_slug':slug, 'lesson_id':uuid}) 

    video_questions_list = video.get_video_questions_context_json()
    template_context['video_questions_list'] = video_questions_list
    return render(request, video_template, template_context)

@login_required
def quiz(request, slug, uuid):
    if not user_allowed_to_access_course(request, slug):
        return redirect(reverse('panel'))

    lesson = get_lesson_or_404(slug, uuid, 'QUIZ')
    next_lesson_dict = lesson.get_next_lesson()

    template_context = initialize_context({'img_url', 'audio_url'})
    template_context.update(next_lesson_dict)

    template_context.update({'course_slug':slug, 'lesson_id':uuid}) 

    quiz_questions_list = lesson.get_quiz_questions_context_json()
    template_context['quiz_questions_list'] = quiz_questions_list
    return render(request, quiz_template, template_context)

@login_required
def assignment(request, slug, uuid):
    if not user_allowed_to_access_course(request, slug):
        return redirect(reverse('panel'))

    lesson = get_lesson_or_404(slug, uuid, 'ASSIGNMENT')

    next_lesson_dict = lesson.get_next_lesson()

    template_context = initialize_context({'img_url', 'audio_url'})
    template_context.update(next_lesson_dict)
    template_context.update({'course_slug':slug, 'lesson_id':uuid}) 

    assignment_details_dict = lesson.get_assignment_details_json()
    template_context['assignment_details_dict'] = assignment_details_dict

    submitted_assignment_qrst = Assignment.objects.filter(lesson=lesson, user=request.user)

    #The student has submitted this assignment
    if submitted_assignment_qrst:
        template_context['assignment_submitted'] = True
        submitted_assignment = submitted_assignment_qrst[0]
        submitted_assignment_details_dict = submitted_assignment.get_assignment_context()
        template_context['submitted_assignment_details_dict'] = submitted_assignment_details_dict
    else:
        template_context['assignment_submitted'] = False

    return render(request, assignment_template, template_context)

@require_POST
def submit_image_assignment(request):
    if request.user.is_authenticated:

        f = Submitted_Assignment_Form(request.POST, request.FILES)
        if f.is_valid():
            slug = f.cleaned_data['course_slug']
            if not user_allowed_to_access_course(request, slug):
                return HttpResponse(status=401)

            uuid = f.cleaned_data['lesson_uuid']
            lesson = get_lesson_or_404(slug, uuid, 'ASSIGNMENT')

            if Assignment.objects.filter(user=request.user, lesson=lesson).exists():
                return HttpResponse(status=403)

            assignment = f.save(commit=False)
            assignment.user = request.user
            
            assignment.lesson = lesson
            assignment.assign_unique_names_to_images()
            assignment.save()

            #Below should be made async;the submitter should not have to wait for this
            create_completed_lesson_record(request.user, lesson, '', assignment)
            return HttpResponse("Success")
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=401)

