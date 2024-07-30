from django.contrib import admin
from django.urls import path
from .views import index, update

urlpatterns = [path("", index),path("<int:id>/", update)]
