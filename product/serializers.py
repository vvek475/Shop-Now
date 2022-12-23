from datetime import date, timedelta

from django.core.exceptions import ObjectDoesNotExist

# rest framewrok
from rest_framework import serializers

# from app directory
from .models import Product, Discount, Count
from .validators import validate_expires_on

class ProductSerializer(serializers.ModelSerializer):
    
    discounted_price=serializers.SerializerMethodField(read_only=True)
    seller_name=serializers.CharField(source='seller.username',read_only=True)
    guarantee_upto=serializers.SerializerMethodField(read_only=True)
    discounts=serializers.SerializerMethodField(read_only=True)
    count=serializers.IntegerField(write_only=True)
    product_count=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        
        model = Product
        fields=['id','name','price','discounted_price','discounts','seller_name','guarantee_upto','count','product_count']
        
    def create(self, validated_data):
        
        seller=self.context.get('request')
        count=validated_data.pop('count')
        
        if seller and seller.user:
            validated_data['seller']=seller.user
            
        instance = super().create(validated_data)
        Count.objects.create(product=instance,count=count)
        
        return instance
        
    
    def get_discounted_price(self,obj):
        
        discount=[]
        
        if obj.discount_set.all():
            [discount.append(i.percentile) for i in obj.discount_set.all()]
            if len(discount):
                disPrice=obj.price-(obj.price/100)*(sum(discount))
                return disPrice
            
        return obj.price
        
    def get_product_count(self,obj):
        try:
            count_object=Count.objects.get(product=obj)
            count={
             'count':count_object.count,
            'refurbished':count_object.refurbished_count 
            }
        except ObjectDoesNotExist:
            count = None
        
        return count
    
    def get_discounts(self,obj):
        
        discounts=[]
        [discounts.append({'name':i.name,'percentile':i.percentile,'expireson':i.expireson}) for i in obj.discount_set.all()]
        
        return discounts
    
    def get_guarantee_upto(self,obj):
        
        expires_on=date.today()+timedelta(days=int(obj.guarantee))
        
        return expires_on
    
class DiscountSerializer(serializers.ModelSerializer):
    
    expireson=serializers.DateField(validators=[validate_expires_on])
    
    class Meta:
        
        model=Discount
        fields=['products','name','percentile','expireson']
