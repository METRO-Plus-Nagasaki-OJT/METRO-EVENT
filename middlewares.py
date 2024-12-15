from django.shortcuts import redirect


class AuthenticatedUser:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cache-Control"] = "no-store"
        response["Pragma"] = "no-cache"
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        skip_middleware = getattr(view_func, "_skip_authenticated_user", False)

        if request.path == "/p-hub-admin/" and request.user.is_authenticated:
            return redirect("menu")

        if skip_middleware:
            return None

        if not request.user.is_authenticated:
            return redirect("login")

        return None
