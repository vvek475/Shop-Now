from django.urls import path
from .views import *

urlpatterns=[
    path('',payment,name='payment'),
    path('paymentHandler',payment_handler,name='payment_handler'),
    path('refund',refund,name='refund')
]