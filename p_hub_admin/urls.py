from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name = "login"),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('participants/<int:event_id>/', views.participants_list, name='participants_list'),
    path("menu/",views.menu,name="menu")
]
