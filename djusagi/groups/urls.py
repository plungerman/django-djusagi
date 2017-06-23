from django.conf.urls import url

from djusagi.groups import views


urlpatterns = [
    # detail view for list and search
    url(
        r'^details/$', views.details, name='groups_details'
    ),
    # home
    url(
        r'^$', views.index, name='groups_home'
    )
]
