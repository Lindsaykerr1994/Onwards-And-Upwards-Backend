from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_appointments, name="all_appointments"),
    path('add_appointment', views.add_app, name="add_app"),
]
