from django.urls import path
from . import views

urlpatterns = [
    path('add/<appointment_number>', views.add_participant_form,
         name="add_part_form"),
]
