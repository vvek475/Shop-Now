# rest framework
from rest_framework import serializers

# base directory
from product.models import Product
from payment.models import Reciept

# app directory
from .models import *

class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Payment
        fields = '__all__'
        
class RefundSerializer(serializers.Serializer):
    
    product = serializers.PrimaryKeyRelatedField(allow_empty=False,write_only=True ,many=True,queryset=Product.objects.all())
    reciept = serializers.PrimaryKeyRelatedField(allow_empty=False,write_only=True ,many=True,queryset=Reciept.objects.all())
