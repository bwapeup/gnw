from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from gnw.models import Course, Unit, Lesson, Lesson_Material
from enrollment.models import Enrollment
from progress.models import Completed_Learning_Materials
from django.http import HttpResponse


def index(request):
    return render(request, 'gnw/index.html',)

def courses_main_page(request):
    return render(request, 'gnw/courses.html',)

@login_required
def panel(request):
    enrolled_classes = Enrollment.objects.filter(user=request.user, is_current=True).select_related('course')
    return render(request, 'gnw/panel.html', {'enrolled_classes':enrolled_classes})

@login_required 
def course(request, slug):
    #Check (1) whether the course requested exists, and (2) whether the user is enrolled in it
    if not Enrollment.objects.filter(user=request.user, course__slug=slug, is_current=True).exists():
        return redirect(reverse('panel'))
    
    course = Course.objects.filter(slug=slug).prefetch_related('unit_set__lesson_set__lesson_material_set').first()

    a = Completed_Learning_Materials.objects
    b = a.filter(enrollment__user=request.user, enrollment__is_current=True, lesson_material__lesson__unit__course__slug=slug)
    clms = b.values_list('lesson_material__random_slug', flat=True)

    download_url = 'gnw/assets/download/'
    template_name = 'gnw/course_main.html'
    context = {'course':course, 'course_name':course.course_name, 'course_slug':slug, 'completed_LMs':clms, 'download_url':download_url}
    return render(request, template_name, context)
    

@login_required
def lecture(request, slug, uuid):
    if not Enrollment.objects.filter(user=request.user, course__slug=slug, is_current=True).exists():
        return redirect(reverse('panel'))

    learning_material = get_object_or_404(Lesson_Material, random_slug=uuid)
    file_name = learning_material.file_name
    next_url_dict = learning_material.get_next_LM_url()
    
    download_url = '/static/gnw/assets/download/'
    
    if 'lecture' in next_url_dict['next_url']:
        next_url = '/panel/my_courses/' + next_url_dict['next_url']
        course_url = ''
    else:
        next_url = download_url + next_url_dict['next_url']
        course_url = '/panel/my_courses/' + learning_material.lesson.unit.course.slug
        
    template_name = 'gnw/' + 'lecture_main.html'
    context = {'file_name':file_name, 'uuid':uuid, 'next_url':next_url, 'next_uuid':next_url_dict['next_uuid'], 'course_url':course_url}
    
    return render(request, template_name, context)

