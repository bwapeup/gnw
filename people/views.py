from .forms import StudentInfoUpdateForm
from .models import Student
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def update_student_info(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
    else:
        return render(request, 'people/update_student_info.html', {'no_student_account':True})
    if request.method == 'POST':
        form = StudentInfoUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'people/update_student_info.html', {'account_update_success':True})
        else:
            return render(request, 'people/update_student_info.html', {'form': form}) 
    else:
        form = StudentInfoUpdateForm(instance=student)
        return render(request, 'people/update_student_info.html', {'form': form})

@login_required
def show_my_info(request):
    context = {}
    if hasattr(request.user, 'student'):
        student = request.user.student
        context['is_student'] = True
        context['mobile'] = student.mobile
        context['parent_name'] = student.parent_name
        context['student_name'] = student.student_name

        if student.student_gender == student.MALE:
            gender = '男'
        elif student.student_gender == student.FEMALE:
            gender = '女'
        else:
            gender = ''
        context['student_gender'] = gender

        if student.student_birth_date is not None:
            context['student_birth_date'] = student.student_birth_date
        else:
            context['student_birth_date'] = ''
        context['city'] = student.city
    else:
        context['is_student'] = False
        if request.user.name != '':
            context['username'] = request.user.name
        else:
            context['username'] = request.user.username
        context['parent_name'] = ''
        context['student_name'] = ''
        context['student_gender'] = ''
        context['student_birth_date'] = ''
        context['city'] = ''

    return render(request, 'people/show_student_info.html', context)
