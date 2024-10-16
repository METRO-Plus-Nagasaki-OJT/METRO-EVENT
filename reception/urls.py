from django.shortcuts import render
from django.urls import path
from . import views

app_name = "reception"
urlpatterns = [
    path("", views.index, name="index"),
    path("client/", views.client, name="client"),
    path("client/v2", views.client_v2, name="client-v2"),
    path("settings", views.settings, name="settings"),
]
