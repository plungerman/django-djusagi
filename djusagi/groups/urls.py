# -*- coding: utf-8 -*-

from django.urls import path
from djusagi.groups import views


urlpatterns = [
    # detail view for list and search
    path('details/', views.details, name='groups_details'),
    # home
    path('', views.index, name='groups_home')
]
