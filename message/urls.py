from django.urls import path
from . import views

urlpatterns = [
    path("", views.message_view, name = "message"),
    path("get_message_data/<int:message_id>/", views.get_message_details, name ="get_message_details"),
    path("autocomplete-suggestions-subject/", views.autocomplete_subject_suggestions, name = "autocomplete_subject_suggestions"),
    path("autocomplete-suggestions-sender/", views.autocomplete_sender_suggestions, name = "autocomplete_sender_suggestions")
]
