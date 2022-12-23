# django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Product(models.Model):
    
    seller=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=255)
    price=models.IntegerField(default=1)
    guarantee=models.IntegerField(default=0) # number of days
    
    def __str__(self):
        
        return self.name
    

class Discount(models.Model):
    
    products=models.ManyToManyField(Product)
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