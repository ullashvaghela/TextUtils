from rest_framework import serializers
from .models import Category,Subcategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        """
        Create and return a new `Category` instance, given the validated data.
        """
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Category` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id','category','name']

    def create(self, validated_data):
        """
        Create and return a new `Subcategory` instance, given the validated data.
        """
        return Subcategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Subcategory` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance