from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import StudentInfoUpdateForm

#Templates:
#--------------------------------------
update_student_info_template = 'people/update_student_info.html'
show_student_info_template = 'people/show_student_info.html'
#--------------------------------------

template_context = {}

@login_required
def update_student_info(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
    else:
        template_context.update({'no_student_account':True})
        return render(request, update_student_info_template, template_context)
    if request.method == 'POST':
        form = StudentInfoUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, '信息更改成功！')
            return redirect(reverse('show_my_info'))
        else:
            template_context.update({'form': form})
            return render(request, update_student_info_template, template_context) 
    else:
        form = StudentInfoUpdateForm(instance=student)
        template_context.update({'form': form})
        return render(request, update_student_info_template, template_context) 

@login_required
def show_my_info(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
        template_context['is_student'] = True
        template_context['mobile'] = request.user.mobile
        template_context['parent_name'] = student.parent_name
        template_context['student_name'] = student.student_name

        if student.student_gender == student.MALE:
            gender = '男'
        elif student.student_gender == student.FEMALE:
            gender = '女'
        else:
            gender = ''
        template_context['student_gender'] = gender

        if student.student_birth_date is not None:
            template_context['student_birth_date'] = student.student_birth_date
        else:
            template_context['student_birth_date'] = ''
        template_context['city'] = student.city
    else:
        template_context['is_student'] = False
        if request.user.name != '':
            template_context['username'] = request.user.name
        else:
            template_context['username'] = request.user.username
        template_context['parent_name'] = ''
        template_context['student_name'] = ''
        template_context['student_gender'] = ''
        template_context['student_birth_date'] = ''
        template_context['city'] = ''

    return render(request, show_student_info_template, template_context)
