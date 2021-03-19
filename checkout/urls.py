from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('<appointment_number>', views.checkout, name="checkout"),
    path('cache_checkout_data/',
         views.cache_checkout_data,
         name='cache_checkout_data'),
    path('checkout_success/<receipt_no>', views.checkout_success,
         name='checkout_success'),
    path('wh/', webhook, name="webhook"),
    path('send_payment_request/<appointment_number>',
         views.send_payment_request, name="send_payment"),
    path('already_paid/<appointment_number>', views.already_paid,
         name="already_paid")
]
