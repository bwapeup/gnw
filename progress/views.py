from django.http import HttpResponse
from django.views.decorators.http import require_POST
from enrollment.models import Enrollment
from gnw.models import Lesson
from progress.models import Completed_Lessons
from django.contrib.auth.decorators import login_required


#AJAX
#======================================================================
@require_POST
@login_required
def ajax_record_completed_lesson(request):
    uuid = request.POST.get('random_slug')
    lesson_results = request.POST.get('results')
    lm = Lesson.objects.filter(random_slug = uuid).first()
    if lm is not None:
        my_enrollment = Enrollment.objects.filter(user=request.user, course=lm.unit.course, is_current=True).first()
        if my_enrollment is not None:
            if Completed_Lessons.objects.filter(enrollment=my_enrollment, lesson=lm).count() < 10:
                Completed_Lessons.objects.create(enrollment=my_enrollment, lesson=lm, results=lesson_results)
                return HttpResponse("Success: record created")
            else:
                return HttpResponse("Error: No record created")
        else:
            return HttpResponse("Error: No record created")
    else:
        return HttpResponse("Error: No record created")           
