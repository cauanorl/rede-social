from django.http import HttpResponseBadRequest


def ajax_required(f):
    def wrapper(request, *args, **kwargs):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not is_ajax:
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__

    return wrapper
