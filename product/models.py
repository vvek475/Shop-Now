# django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.exceptions import ObjectDoesNotExist

from datetime import date, timedelta

# Create your models here.
class Product(models.Model):
    
    seller=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=255)
    price=models.IntegerField(default=1)
    guarantee=models.IntegerField(default=0) # number of days
    
    @property
    def discounted_price(self):
        discount=[]
        
        if self.discount.all():
            [discount.append(i.percentile) for i in self.discount.all()]
            if len(discount):
                disPrice=self.price-(self.price/100)*(sum(discount))
                return disPrice
            
        return self.price
    
    @property
    def product_count(self):
        try:
                count_object=Count.objects.get(product=self)
                return {
                    'count':count_object.count,
                    'refurbished':count_object.refurbished_count 
                }
        except ObjectDoesNotExist:
            return None
    
    @property
    def discounts(self):
        
        discounts=[]
        [discounts.append({'name':i.name,'percentile':i.percentile,'expireson':i.expireson}) for i in self.discount.all()]
        
        return discounts
    @property
    def guarantee_upto(self):
        
        expires_on=date.today()+timedelta(days=int(self.guarantee))
        
        return expires_on
    
    def __str__(self):
        
        return self.name
    

class Discount(models.Model):
    
    products=models.ManyToManyField(Product,related_name='discount')
    name=models.CharField(max_length=255)
    percentile=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)])
    is_active=models.BooleanField(default=False)
    expireson=models.DateField()
    
    def __str__(self):
        
        return self.name
    
    
class Count(models.Model):
    
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    count=models.IntegerField(default=10,validators=[MinValueValidator(1)])
    refurbished_count=models.IntegerField(default=0,validators=[MinValueValidator(0)])
    
    
    def __str__(self) -> str:
        
        return f'{self.product}-{self.count}'