# your_app/middleware.py
from django.contrib.auth import logout
from django.shortcuts import redirect

class SessionHealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and 'thread_id' not in request.session:
            logout(request)
            return redirect('/')  # or 'home'
        return self.get_response(request)
