# django
from django.urls import path

# app directory
from .views import *

urlpatterns=[
    path('',OrderView.as_view({'get':'list','post':'create','put':'update'})), 
    path('kart',KartView.as_view({'post':'update_products','put':'remove_products'})),
    path('checkout',KartView.as_view({'get':'checkout'})),

]