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
    
    '''
    Kart list update destroy remove
    Karts are created per user basis and remain till user exists
    Products are added to karts and later moved to orders
    '''
    
    queryset=Kart.objects.all()
    serializer_class=KartSerializer
    
    def get_kart(self,*args,**kwargs):

        qs=Kart.objects.get(user=self.request.user)
        kart=self.serializer_class(qs)
        return Response(kart.data)

    def update_products(self,*args,**kwargs):
        
        '''
        POST
        List of product ids are passed in body 
        This method adds products to kart
        
        If no products are passed old kart data is returned
        If wrong id passed status code 200 is returned
        '''
        
        qs=self.queryset.get(user=self.request.user)
        data=dict(self.request.data)
        products=data.get('products')
        
        if products:
            products=list(map(int,products))
            qs.products.add(*products)
            qs=self.serializer_class(qs)
            
            return Response(qs.data)
        
        return Response({'warning':'please pass products to add to kart'})
    
    def remove_products(self,*args,**kwargs):
        
        '''
        PUT
        List of product ids are passed in body 
        This method removes products from kart
        
        If no products are passed old kart data is returned
        If wrong id passed Bad request and errors are returned
        '''
        
        data=dict(self.request.data)
        qs=self.queryset.get(user=self.request.user)
        data=data.get('products')
        if data:
            qs.products.remove(*data)
        qs=KartSerializer(qs)
        
        return Response(qs.data)
    
    def checkout(self,*args,**kwargs):
        
        '''
        GET
        A get request is passed to this function
        If user has a active order already then data is passed there
        Else a new Order model is created
        All products from kart is moved to orders
        And Kart is emptied
        '''
        
        user_kart=self.queryset.get(user=self.request.user)
        qs=user_kart.products.all()
        qs=[i.id for i in qs]
        user_order = Order.objects.filter(user=self.request.user,isactive=True)
        
        if user_order:
            user_order=user_order[0]
            user_order=OrderSerializer(user_order,data={'products':qs},partial=True)

        else:
            user_order=OrderSerializer(data={'products':qs},context={'request':self.request})
            
        if user_order.is_valid(raise_exception=True):
            user_order.save()
                
        user_kart.products.clear()
        
        return Response({"order":user_order.data,'payment_url':PAYMENT_URL})
            

class OrderView(ListModelMixin,CreateModelMixin,UpdateModelMixin,GenericViewSet):
    
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    
    '''
    Order list create update
    Order is used for final payment proccess
    Products from Kart is passed here
    Products can only be passed from Kart 
    Or a new order is created with products
    Once payment done Order is set to inactive
    '''
    
    def list(self, request, *args, **kwargs):
        
        qs=get_object_or_404(Order,user=self.request.user,isactive=True)
        qs=self.serializer_class(qs)
        
        return Response(qs.data)

    def create(self, request, *args, **kwargs):
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        '''
        PUT
        This removes products from order 
        If wrong product passed in body Bad request is returned
        If no products are passed old data is returned
        '''
        data=dict(self.request.data)
        qs=self.queryset.get(user=self.request.user)
        data=data.get('products')
        if data:
            qs.products.remove(*data)
        qs=OrderSerializer(qs)
        
        return Response(qs.data)
    
order_view = OrderView.as_view({'get':'list','post':'create','put':'update'})
kart_view = KartView.as_view({'get':'get_kart','post':'update_products','put':'remove_products'})
checkout_view = KartView.as_view({'get':'checkout'})