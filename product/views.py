# rest framework
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

# app directory
from .models import *
from .serializers import *

class ProductView(ListCreateAPIView):
    
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
class ProductConfigure(RetrieveUpdateDestroyAPIView):
    
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'
    
class DiscountView(ListCreateAPIView):
    
    queryset=Discount.objects.all()
    serializer_class=DiscountSerializer
    
