from datetime import date,timedelta

# rest framework
from rest_framework import serializers

def validate_expires_on(ex_date):
    
    if ex_date<date.today()+timedelta(days=1):
        
        raise serializers.ValidationError('Discount period should be valid atleast for a day')

    elif ex_date>date.today()+timedelta(days=20):
        
        raise serializers.ValidationError('Maximum discount valid period is 20 days')