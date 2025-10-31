from django.contrib.auth.views import (
    PasswordResetDoneView
)

from django.shortcuts import redirect

class ProtectedPasswordResetDoneView(PasswordResetDoneView):
    def get(self, request, *args, **kwargs):
        if not request.session.get('reset_requested', False):
            return redirect('index')
        request.session['reset_requested'] = False
        return super().get(request, *args, **kwargs)