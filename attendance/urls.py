from django.urls import path
from .views import index, update, index_v2

urlpatterns = [path("", index,name="attendance"), path("<int:id>/", update), path("v2/", index_v2,name="attendance2")]
