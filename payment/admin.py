# django
from django.contrib import admin

# app directory
from . import models

admin.site.register(models.Payment)
admin.site.register(models.Reciept)
admin.site.register(models.Wallet)