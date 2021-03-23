from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('notifications', views.notifications, name="all_notifications"),
    path('notifications/<note_id>', views.view_notification,
         name="view_notification")
]
