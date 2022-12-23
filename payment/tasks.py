from __future__ import absolute_import,unicode_literals

# celery
from celery import shared_task
from celery.utils.log import get_task_logger

# base directory
from shop_now.celery import app 

# app directory
from .email import send_email
from .models import Reciept

logger = get_task_logger(__name__)

@shared_task
def delivery_status_update(recieptlst):
    
    recieptid=recieptlst
    reciept=Reciept.objects.get(pk=recieptid)
    reciept.status='1'
    reciept.save()
    
    return {'message':'delivery status updated'}


@app.task(name='send_email_task')
def send_email_task(user,total):
    
    logger.info('sent confirmation email')
    
    return send_email(user.user,total)