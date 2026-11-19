from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.create_user, name="create_user"),
    path("notes/", views.create_note, name="create_note"),
    path("notes/list/", views.list_notes, name="list_notes"),
]