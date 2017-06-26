from django.conf.urls import url

from djusagi.reports import views


urlpatterns = [
    # detail view for list and search
    url(
        r'^two-factor-auth/$', views.two_factor_auth, name='two_factor_auth'
    ),
    # home
    url(
        r'^$', views.index, name='reports_home'
    )
]
