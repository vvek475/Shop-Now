# django
from django.urls import reverse

import datetime

# app directory
from product.models import Discount
from product.serializers import ProductSerializer

# mixins
from mixins.mixins_test import AuthenticatedUserTestCase


class TestProductView(AuthenticatedUserTestCase):
    def setUp(self) -> None:
        self.product_list_create=reverse('product-list-create')
        self.product_retrieve_update_destroy=reverse('product-detail-update',args=[1])
        
        product=ProductSerializer(data={'name':'Li-ning','price':1899,'count':20})
        if product.is_valid():
            self.product=product.save()
            
        return super().setUp()
        
    def test_product_list(self):
        response = self.client.get(self.product_list_create, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.status_code,200)
        
    def test_product_create(self):
        product_data={
            'name': 'Li-ning', 'price': 1899, 'id': 2, 'discounted_price': 1899, 
            'discounts': [], 'seller_name': 'admin', 'guarantee_upto': datetime.date.today(),
            'product_count': {'count': 20, 'refurbished': 0}
        }
        response = self.client.post(self.product_list_create, {'name':'Li-ning','price':1899,'count':20}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.data,product_data)
        self.assertEquals(response.status_code,201)
        
    def test_product_retrieve(self):
        response = self.client.get(self.product_retrieve_update_destroy, content_type='application/json' , HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.status_code,200)
        
    def test_product_update(self):
        response = self.client.put(self.product_retrieve_update_destroy,{'name':'Li-ning raquets','price':1899,'count':200}, content_type='application/json' , HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.data['name'],'Li-ning raquets')
        self.assertEquals(response.status_code,200)

    def test_product_destroy(self):
        response = self.client.delete(self.product_retrieve_update_destroy, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.status_code,204)

class TestDiscountView(AuthenticatedUserTestCase):
    def setUp(self) -> None:
        self.discount_url=reverse('discount')
        product=ProductSerializer(data={'name':'Li-ning','price':1899,'count':20})
        if product.is_valid():
            self.product=product.save()
        Discount.objects.create(name='sports',percentile=12,expireson=datetime.date.today()+datetime.timedelta(days=2))
        return super().setUp()
    
    def test_discount_list(self):
        response = self.client.get(self.discount_url,HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEquals(response.status_code,200)
        
    def test_discount_create(self):
        response = self.client.post(self.discount_url,{
            'products':[1],
            'percentile':20,
            'name':'friday',
            'expireson':datetime.date.today()+datetime.timedelta(days=2)
        },HTTP_AUTHORIZATION=f'Bearer {self.token}') 
        self.assertEquals(response.status_code,201)