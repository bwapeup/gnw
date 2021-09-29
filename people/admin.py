from django.contrib import admin
#from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Student
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'name', 'mobile', 'email']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'first_name', 'last_name', 'mobile', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'require_password_change', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'mobile'),
        }),
    )

    search_fields = ('username', 'name', 'mobile', 'first_name', 'last_name', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)

admin.site.unregister(Group)
