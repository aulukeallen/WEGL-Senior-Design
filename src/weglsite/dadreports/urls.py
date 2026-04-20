from django.urls import path
from . import views

app_name = "dadreports"

urlpatterns = [
    path("", views.index, name="index"),
    path("stats/", views.stats, name="stats"),
    path("stats/export", views.export_stats, name='export_stats')
]