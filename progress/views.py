from django.shortcuts import render, redirect
from django.http import HttpResponse
from enrollment.models import Enrollment
#from django.contrib.auth.models import User
from gnw.models import Lesson_Material
from progress.models import Completed_Learning_Materials
from django.core.urlresolvers import reverse


#AJAX
#======================================================================

def ajax_record_completed_lm(request):
    if request.method == 'POST':
        uuid = request.POST.get('random_slug')
        lm = Lesson_Material.objects.filter(random_slug = uuid).first()
        if lm is not None:
            my_enrollment = Enrollment.objects.filter(user=request.user, course=lm.lesson.unit.course, is_current=True).first()
            if my_enrollment is not None:
                if not Completed_Learning_Materials.objects.filter(enrollment=my_enrollment, lesson_material=lm).exists():
                    Completed_Learning_Materials.objects.create(enrollment=my_enrollment, lesson_material=lm)
                    return HttpResponse("record created")
                else:
                    return HttpResponse("record already exists")
            else:
                return HttpResponse("user is not enrolled in course")
        else:
            return HttpResponse("LM doesn't exist")            
    else:
        return HttpResponse("")
