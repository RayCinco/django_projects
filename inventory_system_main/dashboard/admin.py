from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderHistory)
admin.site.register(models.ProductHistory)
admin.site.site_header = "Inventory System Admin"