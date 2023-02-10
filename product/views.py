# rest framework
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

# app directory
from .models import *
from .serializers import *

class ProductView(ListCreateAPIView):
    
    '''
    Products create and list
    '''
    
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
class ProductConfigure(RetrieveUpdateDestroyAPIView):
    
    '''
    Products retrieve and update
    '''
    
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'
    
class DiscountView(ListCreateAPIView):
    
    '''
    Discount list and create
    '''
    
    queryset=Discount.objects.all()
    serializer_class=DiscountSerializer
    
product_list_create = ProductView.as_view()
product_retrieve_update = ProductConfigure.as_view()
discount_list_create = DiscountView.as_view()