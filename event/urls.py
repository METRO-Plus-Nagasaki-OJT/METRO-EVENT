from django.urls import path, include
from . import views
urlpatterns = [
    path("",views.index,name="event"),
    path("updateevent/<int:id>/",views.edit,name="update")
]
