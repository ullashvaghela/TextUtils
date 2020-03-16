from django.shortcuts import render
from djongo.models import Q

# User import.
from .models import Category,Subcategory
from .serializers import CategorySerializer,SubcategorySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser


# Create your views here.
class CategoryList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    """
    List all Category, or create a new Category.
    """
    serializer_class = CategorySerializer          
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `Category Name` query parameter in the URL.
        """
        queryset = Category.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetails(APIView):
    permission_classes = (AllowAny,)
    """
    Retrieve, update or delete a Category instance.
    """
    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Http404
    def get(self,request,pk):
        category = self.get_object(pk)
        serialize=CategorySerializer(category)
        return Response(serialize.data)

    def put(self,request,pk, formate=None):
        category = self.get_object(pk)
        serialize = CategorySerializer(category,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
SubCategory
"""
class SubcatregoryList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    """
    List all Category, or create a new Subategory.
    """
    serializer_class = SubcategorySerializer        
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `Category Name` query parameter in the URL.
        """
        queryset = Subcategory.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

    def post(self, request, format=None):
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubcatregoryDetails(APIView):
    permission_classes = (AllowAny,)
    """
    Retrieve, update or delete a Subcategory instance.
    """
    def get_object(self,pk):
        try:
            return Subcategory.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Http404
    def get(self,request,pk):
        subcategory = self.get_object(pk)
        serialize=SubcategorySerializer(subcategory)
        return Response(serialize.data)

    def put(self,request,pk, formate=None):
        subcategory = self.get_object(pk)
        serialize = SubcategorySerializer(subcategory,data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        subcategory = self.get_object(pk)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)