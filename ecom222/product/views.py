from django.shortcuts import render
from djongo.models import Q

# User import.
from .models import Product
from category.models import Subcategory
from .serializers import ProductSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters,generics
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser

"""
Product
"""
class ProductList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    """
    List all Category, or create a new Subategory.
    """
    # def get(self, request, format=None):
    #     product = Product.objects.all()
    #     serializer = ProductSerializer(product, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer_class = ProductSerializer          
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Product.objects.all()
        query = self.request.query_params.get('query', None)
        print(queryset)
        if query is not None:
            queryset = queryset.filter(Q(name__icontains=query)|Q(discription__icontains=query))
        return queryset

class ProductDetails(APIView):
    permission_classes = (AllowAny,)
    """
    Retrieve, update or delete a Subcategory instance.
    """
    def get_object(self,pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Http404

    def get(self,request,pk):
        product = self.get_object(pk)
        serialize=ProductSerializer(product)
        return Response(serialize.data)

    def put(self,request,pk, formate=None):
        product = self.get_object(pk)
        serialize = ProductSerializer(product,data=request.data)
        print(serialize)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)