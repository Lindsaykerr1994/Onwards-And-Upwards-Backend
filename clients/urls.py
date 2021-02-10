from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_clients, name="all_clients"),
    path('add_client', views.add_client, name="add_client"),
]
