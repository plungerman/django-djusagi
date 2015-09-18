from django.conf import settings

def sitevars(request):
    context = {}
    try:
        context['password_reset_url'] = settings.PASSWORD_RESET_URL
    except:
        pass
    return context
