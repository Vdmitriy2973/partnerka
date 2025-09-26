from django.shortcuts import redirect

class AdminAccessMiddleware:
    """
    Разрешает доступ к /admin только staff-пользователям.
    Остальных редиректит на главную.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin"):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect("/")
        return self.get_response(request)
