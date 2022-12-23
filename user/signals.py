# django
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# base directory
from order.models import Kart
from payment.models import Wallet

def user_config(sender,instance,created,*args,**kwargs):
    
    if created:
        
        Kart.objects.create(user=instance)
        Wallet.objects.create(user=instance,balance=10000)
        
post_save.connect(user_config,sender=User)