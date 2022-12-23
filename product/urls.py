from django.urls import path

from . import views

urlpatterns=[
    path('',views.ProductView.as_view()),
    path('<int:pk>',views.ProductConfigure.as_view()),
    path('discount',views.DiscountView.as_view())
]