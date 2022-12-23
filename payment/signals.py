# django
from django.db.models.signals import post_save

# app directory
from .models import *
from .tasks import delivery_status_update

def RecieptCreation(sender,instance,created,*args,**kwargs):
    
    if created:
        
        reciept=Reciept.objects.create(user=instance.user,payment=instance,status='0')
        delivery_status_update.apply_async([reciept.pk],countdown=120)
    
post_save.connect(RecieptCreation,sender=Payment)