from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticatedUserTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        
        
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = self.client.post(reverse('token_obtain_pair'),{
            'username':'admin',
            'password':'admin123'
        }).data['access']