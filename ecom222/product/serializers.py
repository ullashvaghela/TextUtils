from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id','name', 'subcategory', 'price','sku','quantity','discription','created_date','last_update', 'image','buffer_stoke']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
