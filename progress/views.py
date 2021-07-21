from django.shortcuts import render, redirect
from django.http import HttpResponse
from enrollment.models import Enrollment
#from django.contrib.auth.models import User
from gnw.models import Lesson
from progress.models import Completed_Lessons
from django.urls import reverse


#AJAX
#======================================================================

def ajax_record_completed_lesson(request):
    if request.method == 'POST':
        uuid = request.POST.get('random_slug')
        lm = Lesson.objects.filter(random_slug = uuid).first()
        if lm is not None:
            my_enrollment = Enrollment.objects.filter(user=request.user, course=lm.unit.course, is_current=True).first()
            if my_enrollment is not None:
                if not Completed_Lessons.objects.filter(enrollment=my_enrollment, lesson=lm).exists():
                    Completed_Lessons.objects.create(enrollment=my_enrollment, lesson=lm)
                    return HttpResponse("record created")
                else:
                    return HttpResponse("record already exists")
            else:
                return HttpResponse("user is not enrolled in course")
        else:
            return HttpResponse("LM doesn't exist")            
    else:
        return HttpResponse("")
