from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Subcategory
from catalog.category.models import Category

class SubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.CharField(max_length=100,error_messages={'blank': 'Category may not be blank'})
    name = serializers.CharField(max_length=100,error_messages={'blank': 'Subcategory Name may not be blank.'})
    

    def validate(self, data):
        category = data['category']
        try:
            category = Category.objects.get(id=int(category))
        except ObjectDoesNotExist:
            raise serializers.ValidationError('You Enter Wrong Categoty ID')
        return data
    
    def create(self, validated_data):
        category = Category.objects.get(id=int(validated_data['category']))
        name = validated_data['name']
        subcategory = Subcategory.objects.create(name=name,category=category)
        subcategory.save()
        return subcategory

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance