from django.urls import path
from . import views

app_name = "djrecord"

urlpatterns = [
    path("", views.index, name="index"),
    # path("create/", views.create_dj, name="dj-create"),
    # path("edit/<int:pk>/", views.edit_dj, name="dj-edit"),
    # path("delete/<int:pk>/", views.delete_dj, name="dj-delete"),
]