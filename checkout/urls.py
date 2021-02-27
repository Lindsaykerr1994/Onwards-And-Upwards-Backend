from django.urls import path
from . import views

urlpatterns = [
    path('<appointment_number>', views.checkout, name="checkout"),
    path('checkout_success/<receipt_no>', views.checkout_success,
         name='checkout_success')
]
