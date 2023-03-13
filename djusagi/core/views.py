# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render
from djtools.decorators.auth import group_required


@group_required(settings.ADMINISTRATORS_GROUP)
def home(request):
    """Home page view."""
    return render(request, 'home.html')
