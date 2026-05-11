from django.urls import path
from labb.shortcuts import set_theme_view

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects, name="projects"),
    path("contact/", views.contact, name="contact"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("set-theme/", set_theme_view, name="set_theme"),
]