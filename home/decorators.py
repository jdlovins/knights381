from django.contrib.auth.decorators import login_required
from django.contrib import messages


def custom_login_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated():
            messages.add_message(request, messages.WARNING, "Sorry, You need to login to view this page.")
            return decorated_view_func(request, redirect_field_name='next')  # return redirect to signin

        return function(request, *args, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper
