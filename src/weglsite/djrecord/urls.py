from django.urls import path
from . import views

app_name = "djrecord"

urlpatterns = [
    path("", views.index, name="index"),
    path("attendance/", views.attendance, name="attendance"),
    path("clock_in/", views.clock_in, name="clock_in"),
]