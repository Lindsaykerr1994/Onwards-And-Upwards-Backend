from django.urls import path
from . import views

urlpatterns = [
    path('kitlist_terms/<appointment_number>', views.kitlist_and_terms,
         name="kitlist_and_terms"),
    path('kitlist/<appointment_number>', views.onlykitlist,
         name="onlykitlist"),
    path('add/<appointment_number>', views.add_participant_form,
         name="add_part_form"),
    path('view_participant/<int:partId>',
         views.view_participant, name="view_participant"),
    path('update_raform/<int:part_id>',
         views.update_raform, name="update_raform"),
    path('remove_participant', views.remove_participant,
         name="remove_participant"),
    path('success/<appointment_number>/<int:part_id>',
         views.risk_form_success, name="risk_form_success"),
    path('request_denied/<appointment_number>', views.risk_form_denied,
         name="risk_form_denied"),
    path('delete_raform/<int:part_id>',
         views.delete_raform, name="delete_raform"),
    path('view_pdf/<int:part_id>', views.view_pdf, name="view_raform"),
]
