from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response

from djtools.decorators.auth import group_required


@group_required(settings.ADMINISTRATORS_GROUP)
def home(request):
    """
    Home page view
    """
    return render_to_response(
        "home.html",
        context_instance=RequestContext(request)
    )
