# django
from django.contrib import admin

# app directory
from . import models

admin.site.register(models.Order)
admin.site.register(models.Kart)