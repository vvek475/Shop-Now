# django
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# base directory
from order.models import Order


class Payment(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    raz_payment_id=models.CharField(max_length=255)
    raz_order_id=models.CharField(max_length=255)
    raz_signature=models.CharField(max_length=255)
    order=models.OneToOneField(Order,on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(default=timezone.now)
    
    def __str__(self):
        
        if self.user:
            return f'{self.user.username}-{self.date}'
        
        return f'{self.pk}'
    
    
class Reciept(models.Model):
    # 0 creation
    # 1 celery
    # 2 command
    # 3 refunded
    
    STATUS=[
        ('0','Order Placed'), 
        ('1','Out For Delievery'),
        ('2','Delivered'),
        ('3','Refunded')
    ]
    
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    payment=models.OneToOneField(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    status=models.CharField(choices=STATUS,default='0',max_length=225)
    
    
    def __str__(self):
        
        if self.user:
            return f'{self.user.username}'
        
        return self.status
    
    
class Wallet(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    balance=models.IntegerField(default=10000)
    
    def __str__(self):
        return f'{self.user}-{self.balance}'