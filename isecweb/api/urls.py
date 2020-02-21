from django.urls import path
from . import views as view

urlpatterns = [
    path('', view.index),
    path('teleapi/', view.teleapi, name='tele'),
    path('raspapi/<str:devid>/<str:ftype>', view.receive, name='rasp'),
    path('alert/<str:devid>', view.alert, name='alert'),
]
