from django.conf.urls import url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from djusagi.reports import views


urlpatterns = [
    # detail view for list and search
    url(
        r'^two-factor-auth/$', views.two_factor_auth, name='two_factor_auth'
    ),
    # home
    #url(
        #r'^$', views.index, name='reports_home'
    #)
    url(
        r'^$', RedirectView.as_view(url=reverse_lazy('two_factor_auth'))
    )
]
