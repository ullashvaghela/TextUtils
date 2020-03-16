from app_user.models import User
from .models import Order,CartItem,OrderStatus
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user','ordered_item','name','email','mobile_no','address','city','state','zipcode')

class OrderStatusSerialiser(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ("status")