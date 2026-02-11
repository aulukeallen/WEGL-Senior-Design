from django.urls import path
from . import views

app_name = "attendancetracker"

urlpatterns = [
    path("", views.index, name="index"),
]