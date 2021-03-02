from django.urls import path
from . import views

urlpatterns = [
    path('/submit/<appointment_number>', views.add_participant_form,
         name="submit_risk_form"),
]
