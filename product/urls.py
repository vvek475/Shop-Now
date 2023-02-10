from django.urls import path

from .views import *

urlpatterns=[
    path('',product_list_create,name='product-list-create'),
    path('<int:pk>',product_retrieve_update,name='product-detail-update'),
    path('discount',discount_list_create,name='discount')
]