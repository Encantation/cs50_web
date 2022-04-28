from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("entry_exists", views.index, name="entry_exists"),
    re_path(r'(^\S*)', views.entry),
]
