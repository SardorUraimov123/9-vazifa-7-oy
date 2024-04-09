from django.shortcuts import redirect


def staff_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request,*args, **kwargs)
        else:
            return redirect('front:index')
    return wrapper