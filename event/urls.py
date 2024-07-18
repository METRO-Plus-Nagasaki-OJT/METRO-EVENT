from django.urls import path, include
from . import views
urlpatterns = [
    path("",views.index,name="event"),
    # path('deleteevent/<int:id>/', views.delete, name='delete'),
    path("updateevent/<int:id>/",views.edit,name="update")
]
