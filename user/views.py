# django
from django.contrib.auth.models import User

# rest framework
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView

# base directory
from payment.models import Reciept

# app directory
from .serializers import UserSerializer,RecieptListSerializer
from .permissions import OnlyAllowAnon

class UserCreationView(CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[OnlyAllowAnon]

class RecieptListView(ListAPIView):
    
    queryset=Reciept.objects.all()
    serializer_class=RecieptListSerializer
    
    def get(self, request, *args, **kwargs):
        qs=self.get_queryset().filter(user=request.user)
        qs=self.serializer_class(qs,many=True)
        
        return Response({'reciepts':qs.data})
