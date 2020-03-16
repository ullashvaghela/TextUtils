from django.contrib import admin
from .models import Order,OrderStatus
from django.contrib.auth.models import Group

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.unregister(Group)
