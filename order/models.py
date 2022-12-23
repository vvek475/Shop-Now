# django
from django.db import models
from django.contrib.auth.models import User

# from base directory
from product.models import Product,Discount


class Order(models.Model):
    
    products=models.ManyToManyField(Product)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=1)
    total=models.IntegerField(default=0)
    isactive=models.BooleanField(default=False)
    discount=models.ManyToManyField(Discount)
    date=models.DateField(auto_now_add=True)
    email=models.EmailField(max_length=100)
    
    def __str__(self):
        
        return f'{self.email}-{self.date}'
    
    
class Kart(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product)
    
    def __str__(self):
        
        return f'{self.user.username}-kart'
