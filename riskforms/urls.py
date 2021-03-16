from django.urls import path
from . import views

urlpatterns = [
    path('add/<appointment_number>', views.add_participant_form,
         name="add_part_form"),
    path('view_participant', views.view_participant,
         name="view_participant"),
    path('update_raform/<int:part_id>', views.update_raform,
         name="update_raform"),
    path('remove_participant', views.remove_participant,
         name="remove_participant"),
    path('success/<appointment_number>/<int:part_id>',
         views.risk_form_success, name="risk_form_success"),
    path('request_denied/<appointment_number>', views.risk_form_denied,
         name="risk_form_denied")
]
