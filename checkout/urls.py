from django.urls import path
from . import views

urlpatterns = [
    path('<appointment_number>', views.checkout, name="checkout"),
]
