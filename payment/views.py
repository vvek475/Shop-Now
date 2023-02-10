import datetime

# django imports
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404,redirect

# rest framework
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication

# razorpay
import razorpay

# base directory
from product.models import Count
from order.models import Order,Product
from shop_now.settings import RAZORPAY_ID,RAZORPAY_SECRET_KEY

# app directory
from .models import *
from .serializers import *
from .tasks import send_email_task


# Create your views here.
class paymentView(GenericViewSet):
    
    queryset = Order.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class=PaymentSerializer
    authentication_classes=[SessionAuthentication]
    
    def payment(self,request,*args,**kwargs):
        
        user_order=Order.objects.filter(user=self.request.user,isactive=True)
        
        if len(user_order):
            
            user_order=user_order[0]
            client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET_KEY))
            DATA = {
            "amount": user_order.total*100,
            "currency": "INR",
            "receipt": f"receipt#{user_order.id}",
            }
            data=client.order.create(data=DATA)
            context={'user_order':user_order,'ID':RAZORPAY_ID,'order_id':data.get('id')}
            
            return Response(context,template_name='payment.html')
        
        else:
            
            return Response(template_name='order404.html')

'''
we can pass queryset into serializers and can be handled with .data
if we want to save a data we need to pass them in  data keyword as dictionaries
.is_valid() has to be called before saving the data this will access the data keyword 
for validation if data is not passed it will raise error unmodified data can be accessed 
with .initial_data if validation passed we cam access validated data if it fails we can only
access .data after .is_valid()
data keyword will take only dictionaries 
'''   

@csrf_exempt
def payment_handler(request,*args,**kwargs):
    
    data=dict(request.POST)
    user_order=Order.objects.get(user=request.user,isactive=True)
    user=request.user.id
    raz_payment_id=data.get('razorpay_payment_id')[0]
    raz_order_id=data.get('razorpay_order_id')[0]
    raz_signature=data.get('razorpay_signature')[0]
    
    payment_model=PaymentSerializer(data={'user':user,
                                          'raz_payment_id':raz_payment_id,
                                          'raz_order_id':raz_order_id,
                                          'order':user_order.pk,
                                          'raz_signature':raz_signature})
    
    if payment_model.is_valid(raise_exception=True):
        payment_model=payment_model.save()
        
    wallet=Wallet.objects.get(user=request.user)
    wallet.balance=wallet.balance-user_order.total
    wallet.save()
    user_order.isactive=False
    count_objects=Count.objects.filter(product__in=user_order.products.all())
    
    for i in range(len(count_objects)):
        count_objects[i].count-=1
        
    Count.objects.bulk_update(count_objects,['count'])
    user_order.save()
    send_email_task(request,user_order.total)
    
    return redirect('/payment')


class Refund(GenericViewSet):
    
    queryset=Payment.objects.all()
    serializer_class=RefundSerializer
    permission_classes=[AllowAny]
    
    def refund(self,request,*args,**kwargs):
        
        reciept_id=self.request.data.get('reciept')
        product_id=self.request.data.get('product')
        
        if reciept_id and product_id:
            
            reciept=get_object_or_404(Reciept,pk=reciept_id)
            product=get_object_or_404(Product,pk=product_id)
            guarantee_expiry_date=reciept.payment.date+datetime.timedelta(days=product.guarantee)
            
            if reciept.status=='2' and guarantee_expiry_date>=datetime.date.today():
                
                wallet=Wallet.objects.get(user=request.user)
                new_balance=wallet.balance+reciept.payment.order.total
                wallet.balance=new_balance
                count=Count.objects.get(product=product)
                count.refurbished_count+=1
                reciept.status='3'
                wallet.save()
                count.save()
                reciept.save()
                
                return Response({'updated_balance':new_balance})

            else:
                
                return Response({'message':'Your purchase period has exceeded the guarantee limit'})
            
        return Response({'message':'Please pass a valid reciept Id and product Id'})

payment = paymentView.as_view({'get':'payment'})
payment_handler = payment_handler
refund = Refund.as_view({'post':'refund'})