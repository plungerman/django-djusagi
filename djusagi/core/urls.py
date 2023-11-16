# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import include
from django.urls import path
from djauth.views import loggedout
from django.views import static
from django.views.generic import RedirectView
from django.views.generic import TemplateView
#from djusagi.kalendar import views as cali_views
from djusagi.core import views as core_views
#from djusagi.plus import views as plus_views

import os


admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout',
    ),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout',
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login')),
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    # django admin
    path('rocinante/', admin.site.urls),
    # calendar
    #path('calendar/', cali_views.index, name='calendar_home'),
    # emailsettings
    #path(#'emailsettings/', include('djusagi.emailsettings.urls')),
    # groups
    path('groups/', include('djusagi.groups.urls')),
    # groups
    #path('reports/', include('djusagi.reports.urls')),
    # home
    path('', core_views.home, name='home'),
]

# not ready for prime time
    #url(r'^static/(?P<path>.*)$', static.serve,
    #    {'document_root': os.path.join(os.path.dirname(__file__), 'static')}
    #),
    # google+
    #url(
    #    r'^plus/$', plus_views.index,
    #    name='plus_home'
    #),
    # OAuth2
    #url(
    #    r'^oauth2-callback', plus_views.auth_return,
    #    name='oauth2_callback'
    #),
    #url(
    #    r'^oauth2-callback', 'djusagi.core.views.oauth2_callback',
    #    name="oauth2_callback"
    #),
