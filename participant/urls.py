# participants/urls.py
from django.urls import path
from . import views
from .views import get_participant_data

urlpatterns = [
    path('get_participant_data/<int:participant_id>/', get_participant_data, name='get_participant_data'),
    path('', views.participant, name='participant'),

]
