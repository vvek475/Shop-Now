from mixins.mixins_test import AuthenticatedUserTestCase
import datetime
from collections import OrderedDict
from order.serializers import OrderSerializer,KartSerializer, Order
from product.serializers import ProductSerializer

class TestKartSerializer(AuthenticatedUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        
        if product.is_valid(raise_exception=True):
            self.product=product.save()
        self.user.kart.products.add(1)
        
    def test_kart_creation(self):
        # with data
        kart=KartSerializer(data={'products':['1']})
        self.assertEquals(kart.is_valid(),True)
        
        # without data
        kart=KartSerializer(data={})
        self.assertEquals(kart.is_valid(),False)
        self.assertEquals(list(kart.errors.keys())[0],'products')
        
    def test_kart_read_data(self):
        kart=KartSerializer(self.user.kart)
        self.assertEquals(kart.data,{
            'products_list': [OrderedDict([('name', 'Boat TW 200'),
                                           ('price', 2499), ('id', 1), 
                                           ('discounted_price', 2499), 
                                           ('discounts', []),
                                           ('guarantee_upto', datetime.date(2023, 1, 31)),
                                           ('product_count', {'count': 200, 'refurbished': 0})])
                              ]
        })
        
        
class TestOrderSerializer(AuthenticatedUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        
        if product.is_valid(raise_exception=True):
            self.product=product.save()
            
    def test_order_creation(self):
        order=OrderSerializer(data={'products':['1']},context={'request':self})
        self.assertEquals(order.is_valid(raise_exception=True),True)
        order=order.save()
        
        self.order_update()
        
    def order_update(self):
        order=Order.objects.first()
        product=ProductSerializer(data={'name':'Boat TW 200','count':200,'price':2499})
        
        if product.is_valid(raise_exception=True):
            self.product=product.save()
        order=OrderSerializer(order,data={'products':['2']})
        self.assertEqual(order.is_valid(raise_exception=True),True)
        order=order.save()
        order=OrderSerializer(order)
        self.assertEquals(order.data,{
            'total': 4998, 
            'isactive': True, 
            'email': 'admin@admin.com', 
            'date': '2023-01-31', 
            'products_list': 
                [OrderedDict([('name', 'Boat TW 200'), 
                              ('price', 2499), ('id', 1), 
                              ('discounted_price', 2499), 
                              ('discounts', []), 
                              ('guarantee_upto', datetime.date(2023, 1, 31)), 
                              ('product_count', {'count': 200, 'refurbished': 0})
                              ]), 
                 OrderedDict([('name', 'Boat TW 200'), 
                              ('price', 2499), 
                              ('id', 2), 
                              ('discounted_price', 2499), 
                              ('discounts', []), 
                              ('guarantee_upto', datetime.date(2023, 1, 31)), 
                              ('product_count', {'count': 200, 'refurbished': 0})
                              ])
                 ],
                'discount': []
        })