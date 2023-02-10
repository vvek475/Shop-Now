# django
from django.urls import path

# app directory
from .views import *

urlpatterns=[
    path('', order_view, name='order_list_create_update'), 
    path('kart', kart_view, name='kart_get_post_put'),
    path('checkout', checkout_view, name='kart_checkout'),
]