from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_clients, name="all_clients"),
    path('view_client/<int:client_id>', views.view_client,
         name="view_client"),
    path('add_client', views.add_client, name="add_client"),
    path('edit_client/<int:client_id>', views.edit_client, name="edit_client"),
    path('delete_client/<int:client_id>', views.delete_client,
         name="delete_client"),
    path('convert_to_client',
         views.convert_client, name="convert_client"),
]
