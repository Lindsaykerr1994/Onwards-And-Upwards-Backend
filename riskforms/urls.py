from django.urls import path
from . import views

urlpatterns = [
    path('add/<appointment_number>', views.add_participant_form,
         name="add_part_form"),
    path('view_participant/<int:part_id>', views.view_participant,
         name="view_participant"),
    path('success/<int:part_id>', views.risk_form_success,
         name="risk_form_success"),
    path('request_denied/<appointment_number>', views.risk_form_denied,
         name="risk_form_denied")
]
