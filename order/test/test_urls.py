from django.test import SimpleTestCase
from django.urls import reverse,resolve
from order.views import *

class TestProductUrls(SimpleTestCase):
    def setUp(self) -> None:
        self.kart_url=reverse('kart_get_post_put')
        self.order_url=reverse('order_list_create_update')
        return super().setUp()
    
    # def test_kart_list(self):
    #     self.assertEquals(resolve(self.kart_url).func.view_class,KartView)
        
    # def test_order_list(self):
    #     self.assertEquals(resolve(self.order_url).func.view_class,OrderView)