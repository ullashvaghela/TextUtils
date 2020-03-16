from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Cart
from product.models import Product
from rest_framework import serializers

class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.CharField(max_length=20,required=False)
    item_quantity = serializers.IntegerField(default=1)

    def validate(self, data):
        product = self.context.get("product")
        try:
            product = Product.objects.get(id=product)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Product Not Found')
        return data
   
    def create(self, validated_data):
        user = self.context.get("user")
        product = Product.objects.get(id=self.context.get("product"))
        item_quantity = validated_data['item_quantity']

        cart = Cart.objects.create(user=user,product=product,item_quantity=item_quantity)
        cart.save()
        return cart
    
    def update(self,instance, validated_data):
        instance.product.id = self.context.get("product")
        instance.item_quantity = validated_data.get('item_quantity', instance.item_quantity)
        instance.save()
        return instance  