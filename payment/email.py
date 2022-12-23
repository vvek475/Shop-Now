# django
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_email(user,total):
    
    context={
        'name':user.username,
        'email':user.email,
        'total':total
    }
    
    email_subject = 'Order placed'
    email_body = render_to_string('email_message.txt',context=context)
    email=EmailMessage(
        email_subject,email_body,
        settings.DEFAULT_FROM_EMAIL,[user.email,],
    )
    
    return email.send(fail_silently=False)