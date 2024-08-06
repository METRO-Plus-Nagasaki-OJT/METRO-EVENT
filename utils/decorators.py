
from functools import wraps

def authenticated_user_exempt(view_func):
    setattr(view_func, '_skip_authenticated_user', True)
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view