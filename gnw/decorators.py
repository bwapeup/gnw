from django.shortcuts import redirect
from django.urls import reverse

def force_password_change_if_required(view):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.require_password_change:
            return redirect(reverse('require_password_change'))
        else:
            return view(request, *args, **kwargs)
    return wrap