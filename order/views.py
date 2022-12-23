# django
from django.shortcuts import get_object_or_404

# rest framework
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,ListModelMixin,UpdateModelMixin

# base directory
from shop_now.settings import PAYMENT_URL

# app directory
from .models import Order,Kart
from .serializers import OrderSerializer,KartSerializer

class KartView(GenericViewSet):
    
    queryset=Kart.objects.all()
    serializer_class=KartSerializer
    
    def update_products(self,*args,**kwargs):
        
        qs=self.queryset.get(user=self.request.user)
        data=dict(self.request.data)
        products=data.get('products')
        
        if products:
            products=list(map(int,products))
            qs.products.add(*products)
            qs=self.serializer_class(qs)
            
            return Response(qs.data)
        
        return Response({'warning':'please pass products to add to kart'})
    
    
    def checkout(self,*args,**kwargs):
        
        # kart-> products -> order
        user_kart=self.queryset.get(user=self.request.user)
        qs=user_kart.products.all()
        qs=[i.id for i in qs]
        user_order = Order.objects.filter(user=self.request.user,isactive=True)
        
        if user_order:
            user_order=user_order[0]
            user_order=OrderSerializer(user_order,data={'products':qs},partial=True)
            
            if user_order.is_valid(raise_exception=True):
                user_order.save()

        else:
            user_order=OrderSerializer(data={'products':qs},context={'request':self.request})
            
            if user_order.is_valid(raise_exception=True):
                user_order.save()
                
        user_kart.products.clear()
        
        return Response({"order":user_order.data,'payment_url':PAYMENT_URL})
            
    
    
    def remove_products(self,*args,**kwargs):
        
        data=dict(self.request.data)
        qs=self.queryset.get(user=self.request.user)
        qs.products.remove(*data['products'])
        qs=KartSerializer(qs)
        
        return Response(qs.data)

class OrderView(ListModelMixin,CreateModelMixin,UpdateModelMixin,GenericViewSet):
    
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    
    
    def list(self, request, *args, **kwargs):
        qs=get_object_or_404(Order,user=self.request.user,isactive=True)
        qs=self.serializer_class(qs)
        
        return Response(qs.data)

    def create(self, request, *args, **kwargs):
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        
        data=dict(self.request.data)
        qs=self.queryset.get(user=self.request.user)
        qs.products.remove(*data['products'])
        qs=OrderSerializer(qs)
        
        return Response(qs.data)