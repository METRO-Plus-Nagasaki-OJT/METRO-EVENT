# participants/urls.py
from django.urls import path
from . import views
from .views import get_participant_data

urlpatterns = [
    path('delete/<int:participant_id>/', views.delete_participant, name='delete_participant'),
    path('get_participant_data/<int:participant_id>/', get_participant_data, name='get_participant_data'),
    path('participant/update/<int:participant_id>/', views.update_participant, name='update_participant'),
    path('', views.participant, name='participant'),
    path('search/', views.participants_view, name='participant'),

]
