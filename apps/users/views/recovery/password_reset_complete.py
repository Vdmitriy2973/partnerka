from django.contrib.auth.views import (
    PasswordResetCompleteView
)

from django.shortcuts import redirect

class ProtectedPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        if not request.session.get('reset_confirmed', False):
            return redirect("index")
        request.session['reset_confirmed'] = False
        return super().get(request, *args, **kwargs)