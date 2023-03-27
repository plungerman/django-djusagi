# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.views import static
from djauth.views import loggedout
#from djusagi.kalendar import views as cali_views
from djusagi.core import views as core_views
#from djusagi.plus import views as plus_views

import os

urlpatterns = [
    # calendar
    #path('calendar/', cali_views.index, name='calendar_home'),
    # emailsettings
    #path(#'emailsettings/', include('djusagi.emailsettings.urls')),
    # groups
    path('groups/', include('djusagi.groups.urls')),
    # groups
    #path('reports/', include('djusagi.reports.urls')),
    # django auth
    #path(
        #'accounts/login/',
        #auth_views.login,
        #{'template_name': 'accounts/login.html'},
        #name='auth_login',
    #),
    #path(
        #'accounts/logout/',
        #auth_views.logout,
        #{'next_page': '{0}accounts/loggedout/'.format(settings.ROOT_URL)},
        #name='auth_logout',
    #),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout',
    ),
    path('accounts/', RedirectView.as_view(url=settings.ROOT_URL)),
    # home
    path('', core_views.home, name='home'),
]

# not ready for prime time
    # admin
    #(r'^admin/', include(admin.site.urls) ),
    #url(r'^static/(?P<path>.*)$', static.serve,
    #    {'document_root': os.path.join(os.path.dirname(__file__), 'static')}
    #),
    # admin/docs
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
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
