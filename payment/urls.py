from django.urls import path
from .views import *

urlpatterns=[
    path('',paymentView.as_view({'get':'payment'})),
    path('paymentHandler',payment_handler),
    path('refund',Refund.as_view({'post':'refund'}))
]