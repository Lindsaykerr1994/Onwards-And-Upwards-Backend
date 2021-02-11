from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_clients, name="all_clients"),
    path('view_client/<int:client_id>/', views.view_client,
         name="view_client"),
    path('add_client/', views.add_client, name="add_client"),
]
