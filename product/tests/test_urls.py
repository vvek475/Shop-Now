from django.test import SimpleTestCase
from django.urls import reverse,resolve
from product.views import *

class TestProductUrls(SimpleTestCase):
    
    def test_product_list_create_url(self):
        url = reverse('product-list-create')
        self.assertEquals(resolve(url).func.view_class,ProductView)
        
    def test_product_retrieve_update_url(self):
        url = reverse('product-detail-update',args=['1'])
        self.assertEquals(resolve(url).func.view_class,ProductConfigure)
        
    def test_discount(self):
        url = reverse('discount')
        self.assertEquals(resolve(url).func.view_class,DiscountView)
