# django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,User

# base directory
from payment.models import Reciept


class Command(BaseCommand):
    help='comand to check for guest user and delete them'
    
    def handle(self,*args,**kwargs):
        qs=Reciept.objects.all().filter(status='1')
        for i in range(len(qs)):
            qs[i].status='2'
            user_group=qs[i].user.groups.all()[0]
            group=Group.objects.all().filter(name='guest')[0]
            if user_group.name==group.name:
                user_qs= User.objects.get(pk=qs[i].user.pk)
                user_qs.delete()
            
            
        Reciept.objects.bulk_update(qs,['status'])
        
        
        
        self.stdout.write(self.style.SUCCESS('Successfully closed deliveries'))