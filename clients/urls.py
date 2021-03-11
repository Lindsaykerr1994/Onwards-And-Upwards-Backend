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
    path('convert_to_client/new/<int:participant_id>',
         views.convert_new_client, name="convert_new_client"),
    path('convert_to_client/existing/<int:client_id>/<int:participant_id>',
         views.convert_existing_client, name="convert_existing_client")
]
