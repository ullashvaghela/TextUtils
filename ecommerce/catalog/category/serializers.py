from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100,error_messages={'blank': 'Category Name may not be blank.'})

    def create(self, validated_data):
        name = validated_data['name']
        category = Category.objects.create(name=name)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance