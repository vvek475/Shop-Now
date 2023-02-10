# rest framework
from rest_framework import serializers

# base directory
from product.serializers import ProductSerializer
from product.models import Product

# app directory
from . models import Order,Kart
class KartSerializer(serializers.ModelSerializer):
    
    products_list=ProductSerializer(source='products',many=True,read_only=True)
    products=serializers.PrimaryKeyRelatedField(allow_empty=False, many=True,write_only=True,queryset=Product.objects.all())
    
    class Meta:
        
        model=Kart
        fields=['products','products_list']

class OrderSerializer(serializers.ModelSerializer):
    
    # read only
    products_list=ProductSerializer(source='products',many=True,read_only=True)
    email=serializers.EmailField(read_only=True)
    total=serializers.IntegerField(read_only=True)
    isactive=serializers.BooleanField(read_only=True)
    discount=serializers.SerializerMethodField(read_only=True)
    
    # write only
    products=serializers.PrimaryKeyRelatedField(allow_empty=False,write_only=True ,many=True,queryset=Product.objects.all())
    
    class Meta:
        
        model=Order
        fields=['products','total','isactive','email','date','products_list','discount']
        
    def create(self, validated_data):
        
        user=self.context['request'].user
        order=Order.objects.filter(user=user,isactive=True)
        
        if order and order[0].isactive:
            
            return self.update(order[0],validated_data=validated_data)
        
        total=[]
        user_order=ProductSerializer(data=validated_data['products'],many=True)
        
        if user_order.is_valid():
            
            pass
        
        [total.append(int(i['discounted_price'])) for i in user_order.data]
        validated_data['total']=sum(total)
        validated_data['user']=user
        validated_data['email']=user.email
        validated_data['isactive']=True
        validated_data['discount']=self.get_discount(validated_data)
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        
        total=[]
        validated_data['products']=validated_data['products']+list(instance.products.all())
        discount=self.get_discount(validated_data)
        validated_data['discount']=discount
        validated_data=super().update(instance, validated_data)
        user_order=ProductSerializer(data=validated_data.products,many=True)
        
        if user_order.is_valid():
            pass
        
        [total.append(int(i['discounted_price'])) for i in user_order.data]
        validated_data.total=sum(total)
        validated_data.save()
        
        return validated_data
    
    def get_discount(self,dictionary):
        
        discount=[]
        try:
            products=[i for i in dictionary['products']]
        except TypeError:
            products=[i for i in dictionary.products.all()]
        [discount.extend(i.discount.all()) for i in products]
        
        return list(set(discount))