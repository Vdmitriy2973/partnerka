from django.contrib.auth.views import (
    PasswordResetConfirmView
)


class ProtectedPasswordResetConfirmView(PasswordResetConfirmView):
    def get(self, request, *args, **kwargs):
        
        request.session['reset_confirmed'] = True
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        request.session['reset_confirmed'] = True
        return super().post(request, *args, **kwargs)