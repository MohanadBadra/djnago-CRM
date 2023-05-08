from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                if request.user.groups.all()[0].name in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponse('<h1>Access Denied | Register as an other Group</h1>')
        return wrapper_func
    return decorator

def admins_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return view_func(request, *args, **kwargs)
            elif group == 'customer':
                return redirect('user')
    return wrapper_function