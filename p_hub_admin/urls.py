from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name = "login"),
    path("menu/",views.menu,name="menu")
]
