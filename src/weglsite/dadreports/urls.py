from django.urls import path
from . import views

app_name = "dadreports"

urlpatterns = [
    path("", views.index, name="index"),
]