from django.contrib.auth.views import (
    PasswordResetView
)

class ProtectedPasswordResetView(PasswordResetView):
    def get(self, request, *args, **kwargs):
        request.session['reset_requested'] = True
        return super().get(request, *args, **kwargs)