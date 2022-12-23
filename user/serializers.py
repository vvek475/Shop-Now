# django
from django.contrib.auth.models import User,Group

# rest framework
from rest_framework import serializers

# base directory
from payment.models import Reciept
from order.serializers import OrderSerializer

class PaymentInlineSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    order=OrderSerializer(read_only=True)
    

class UserSerializer(serializers.ModelSerializer):
    
    group=serializers.ChoiceField(choices={'guest':'guest','user':'user'},write_only=True)
    
    class Meta:
        
        model=User
        fields=['username','email','password','group']
        
    def create(self, validated_data):
        
        group=validated_data.pop('group')
        group_model,created=Group.objects.get_or_create(name=group)
        instance = super().create(validated_data)
        instance.groups.add(group_model)
        
        return instance
    
class RecieptListSerializer(serializers.ModelSerializer):
    
    payment = PaymentInlineSerializer(read_only=True)
    
    class Meta:
        
        model=Reciept
        fields=['payment']