from django.contrib.auth.models import User
from .models import CartItem
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('user','product','item_quantity')
    