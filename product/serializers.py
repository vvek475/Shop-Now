from datetime import date, timedelta

# rest framewrok
from rest_framework import serializers

# from app directory
from .models import Product, Discount, Count
from .validators import validate_expires_on

class ProductSerializer(serializers.ModelSerializer):
    
    # read only
    seller_name=serializers.CharField(source='seller.username',read_only=True)

    # write only
    count=serializers.IntegerField(write_only=True)
    
    class Meta:
        
        model = Product
        fields=[
                'name', 'price', 'count',
                
                'id', 'discounted_price', 'discounts','seller_name','guarantee_upto', 'product_count'
                ]
        
    def create(self, validated_data):
        
        seller=self.context.get('request')
        count=int(validated_data.pop('count'))
        
        if seller and seller.user:
            validated_data['seller']=seller.user
            
        instance = super().create(validated_data)
        Count.objects.create(product=instance,count=count)
        
        return instance
    
    def update(self, instance, validated_data):
        count=instance.count
        count.count=int(validated_data.pop('count'))
        validated_data['count']=count

        return super().update(instance, validated_data)
    
class DiscountSerializer(serializers.ModelSerializer):
    
    expireson=serializers.DateField(validators=[validate_expires_on])
    
    class Meta:
        
        model=Discount
        fields=['products','name','percentile','expireson']
