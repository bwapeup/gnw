from django.http import HttpResponse
from django.views.decorators.http import require_POST
from enrollment.models import Enrollment
from gnw.models import Lesson
from progress.models import Completed_Lessons


#AJAX
#======================================================================
@require_POST
def ajax_record_completed_lesson(request):
    if request.user.is_authenticated and not request.user.require_password_change:
        uuid = request.POST.get('random_slug')
        lesson_results = request.POST.get('results')
        lm = Lesson.objects.filter(random_slug = uuid).first()
        if lm is not None:
            my_enrollment = Enrollment.objects.filter(user=request.user, course=lm.unit.course, is_current=True).first()
            if my_enrollment is not None:
                if not Completed_Lessons.objects.filter(enrollment=my_enrollment, lesson=lm).exists():
                    Completed_Lessons.objects.create(enrollment=my_enrollment, lesson=lm, results=lesson_results)
                    return HttpResponse("Success: record created")
                else:
                    return HttpResponse("Error: No record created")
            else:
                return HttpResponse("Error: No record created")
        else:
            return HttpResponse("Error: No record created")  
    else:
        return HttpResponse(status=401)         


#Internal Function: Below is only accessible by other view functions
#Make sure that user credentials and request validity have already been verified elsewhere
#Make it async
#======================================================================
def create_completed_lesson_record(user, lesson, results, assignment):
    my_enrollment = Enrollment.objects.filter(user=user, course=lesson.unit.course, is_current=True).first()
    if my_enrollment is not None:
        if not Completed_Lessons.objects.filter(enrollment=my_enrollment, lesson=lesson).exists():
            Completed_Lessons.objects.create(enrollment=my_enrollment, lesson=lesson, results=results, assignment=assignment)
            return True
        else:
            return False
    else:
        return False