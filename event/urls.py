from django.urls import path, include
from . import views
urlpatterns = [
    path("",views.index,name="event"),
    # path('deleteevent/<int:id>/', views.delete, name='delete'),
    path("updateevent/<int:id>/",views.edit,name="update"),
    path("v2/", views.index_v2,name="event2"),
    path("<int:id>/update/v2", views.update_v2)
]
