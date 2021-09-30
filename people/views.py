from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from gnw.decorators import force_password_change_if_required
from .forms import StudentInfoUpdateForm

#Templates:
#--------------------------------------
update_student_info_template = 'people/update_student_info.html'
show_student_info_template = 'people/show_student_info.html'
#--------------------------------------

@force_password_change_if_required
@login_required
def update_student_info(request):
    template_context = {}
    if hasattr(request.user, 'student'):
        student = request.user.student
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
    else:
        if request.method == 'POST':
            form = StudentInfoUpdateForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.user = request.user
                student.save()
                messages.success(request, '信息更改成功！')
                return redirect(reverse('show_my_info'))
            else:
                template_context.update({'form': form})
                return render(request, update_student_info_template, template_context) 
        else:
            form = StudentInfoUpdateForm()
            template_context.update({'form': form})
            return render(request, update_student_info_template, template_context)

@force_password_change_if_required
@login_required
def show_my_info(request):
    template_context = {}
    template_context['mobile'] = request.user.mobile
    if hasattr(request.user, 'student'):
        student = request.user.student
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
        template_context['parent_name'] = ''
        template_context['student_name'] = ''
        template_context['student_gender'] = ''
        template_context['student_birth_date'] = ''
        template_context['city'] = ''

    return render(request, show_student_info_template, template_context)
