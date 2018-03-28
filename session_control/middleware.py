from django.contrib.sessions.models import Session
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from importlib import import_module
from session_control.models import Session_Control

engine = import_module(settings.SESSION_ENGINE)

class PreventConcurrentLoginsMiddleware(MiddlewareMixin):
    """
    Middleware that prevents multiple concurrent logins.
    If a user logs in under the same account that has an active session,
    the existing user's session is cleared and the user is logged out, and the
    new comer takes over.
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            key_from_cookie = request.session.session_key
            if hasattr(request.user, 'session_control'):
                session_key_in_visitor_db = request.user.session_control.session_key
                if session_key_in_visitor_db != key_from_cookie:
                    # Delete the Session object from database and cache
                    engine.SessionStore(session_key_in_visitor_db).delete()
                    request.user.session_control.session_key = key_from_cookie
                    request.user.session_control.save()
            else:
                Session_Control.objects.create(user=request.user, session_key=key_from_cookie)
