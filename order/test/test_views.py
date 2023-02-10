from django.urls import reverse

from order.serializers import OrderSerializer,KartSerializer, Order
from product.serializers import ProductSerializer
from mixins.mixins_test import AuthenticatedUserTestCase

class TestKartView(AuthenticatedUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.kart_url=reverse('kart_get_post_put')
        self.checkout_url=reverse('kart_checkout')
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        
        if product.is_valid(raise_exception=True):
            self.product=product.save()
        self.kart=self.user.kart
        self.kart.products.add(1)
        self.kart_data = KartSerializer(self.kart)

    def test_kart_view_list(self):
        response = self.client.get(self.kart_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data,self.kart_data.data)
        
    def test_kart_view_create(self):
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        
        if product.is_valid(raise_exception=True):
            self.product=product.save()
        response = self.client.post(self.kart_url, {'products':['2']},HTTP_AUTHORIZATION=f'Bearer {self.token}')
        kart_data = KartSerializer(self.kart)
        self.assertEquals(response.data,dict(kart_data.data))
        
    def test_kart_view_update(self):
        
        # with products
        response=self.client.put(self.kart_url, {'products':['2']}, content_type='application/json',HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.data,self.kart_data.data)
        
        # with no products
        response=self.client.put(self.kart_url, content_type='application/json',HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.data,self.kart_data.data)
    
    def test_checkout(self):
        kart_data=self.kart_data.data['products_list']
        response = self.client.get(self.checkout_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # kart Emptied
        self.assertEquals(self.user.kart.products.first(),None)
        
        # order created
        data=response.data['order']['products_list']
        order=OrderSerializer(Order.objects.get(user=self.user))
        self.assertEquals(data,kart_data,order['products_list'])
        
        
        
class TestOrder(AuthenticatedUserTestCase):
    def setUp(self) -> None:
        
        super().setUp()
        self.order_url=reverse('order_list_create_update')
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        
        if product.is_valid(raise_exception=True):
            self.product=product.save()
        order=OrderSerializer(data={'products':['1']},context={'request':self})
        if order.is_valid(raise_exception=True):
            self.order=order.save()
        self.order_data=OrderSerializer(self.order)
        


    def test_order_list(self):
        response=self.client.get(self.order_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.data,dict(self.order_data.data))
        
    def test_order_create(self):
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        
        if product.is_valid(raise_exception=True):
            product=product.save()
            
        # with data
        response = self.client.post(self.order_url, {'products':['2']},HTTP_AUTHORIZATION=f'Bearer {self.token}')
        order_data=OrderSerializer(Order.objects.get(user=self.user))
        self.assertEquals(response.data,order_data.data)
        
        # with no data
        response = self.client.post(self.order_url,HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.status_code,400)
        
        # with wrong data
        response = self.client.post(self.order_url, {'products':['3']},HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.status_code,400)

    
    def test_order_destroy(self):
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        order=OrderSerializer(data={'products':['2']},context={'request':self})
        
        if product.is_valid(raise_exception=True):
            product=product.save()
            
        if order.is_valid(raise_exception=True):
            self.order=order.save()
        
        # with no data
        response = self.client.put(self.order_url, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(len(response.data['products_list']),2)
        
        # with data
        response = self.client.put(self.order_url, {'products':['2']}, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(len(response.data['products_list']),1)
        
        # with wrong data
        response = self.client.put(self.order_url, {'products':['3']}, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(len(response.data['products_list']),1)
        
