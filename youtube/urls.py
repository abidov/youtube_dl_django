from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('download/<str:mp3_id>', download, name='download')
]
