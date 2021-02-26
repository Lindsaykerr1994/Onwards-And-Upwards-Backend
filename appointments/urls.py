from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_appointments, name="all_appointments"),
    path('view_appointment/<appointment_number>', views.view_appoinment,
         name="view_app"),
    path('add_appointment', views.add_app, name="add_app"),
    path('add_appointment/<int:client_id>', views.add_app_w_client,
         name="add_app_w_client"),
    path('edit_appointment/<appointment_number>', views.edit_app,
         name="edit_app"),
    path('delete_appointment/<appointment_number>', views.delete_app,
         name="delete_app")
]
