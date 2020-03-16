from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Product
from catalog.subcategory.models import Subcategory

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100,error_messages={'blank': 'Product Name may not be blank.'})
    subcategory = serializers.CharField(max_length=100,error_messages={'blank': 'Subcategory may not be blank'})
    price = serializers.IntegerField()
    sku = serializers.CharField(max_length=100,error_messages={'blank': 'SKU may not be blank.'})
    quantity = serializers.IntegerField()
    description = serializers.CharField(max_length=500,error_messages={'blank': 'Description may not be blank.'})
    buffer_quantity = serializers.IntegerField()
    image =serializers.ImageField(max_length=None,error_messages={'blank': 'Please Upload Product Image.'})
    
    def validate(self, data):
        subcategory = data['subcategory']
        try:
            subcategory = Subcategory.objects.get(id=subcategory)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('You Enter Wrong Subcategoty ID')
        return data

    def create(self, validated_data):

        name = validated_data['name']
        subcategory = Subcategory.objects.get(id=int(validated_data['subcategory']))
        price = validated_data['price']
        sku = validated_data['sku']
        quantity = validated_data['quantity']
        description = validated_data['description']
        buffer_quantity = validated_data['buffer_quantity']
        image = validated_data['image']
        product = Product.objects.create(name=name,subcategory=subcategory,price=price,sku=sku,quantity=quantity,description=description,buffer_quantity=buffer_quantity,image=image)
        product.save()
        return product
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.subcategory.id = validated_data.get('subcategory', instance.subcategory)
        instance.price = validated_data.get('price', instance.price)
        instance.sku = validated_data.get('sku', instance.sku)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.description = validated_data.get('description', instance.description)
        instance.buffer_quantity = validated_data.get('buffer_quantity', instance.buffer_quantity)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
    # def validate_id(self, value):
    #     if self.instance and value != self.instance.id:
    #         raise serializers.ValidationError("Till death do us part!")
    #     return value