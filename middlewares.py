# middlewares.py

from django.http import HttpResponseForbidden
class AuthenticatedUser:
    """
    Middleware class for verifying whether the user is authenticated or not.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Verifies the user's authentication status
        """
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        skip_middleware = getattr(view_func, "_skip_authenticated_user", False)
        if skip_middleware:
            return None
 
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
 
        return None