from django.shortcuts import render
from djongo.models import Q
from .models import Product
from .serializers import ProductSerializer
from account.models import User

from django.http import Http404
from base.helper import BaseAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser

from base import methods

# Create your views here.

class ProductView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer          
    
    def get(self,request,query=None):
        if query:
            product = Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        else:
            product = Product.objects.all()
        serialize=ProductSerializer(product,many=True)
        response = methods.getPositiveResponse("List of Products",status.HTTP_200_OK,serialize.data)
        return Response(response,status=response['statusCode'])    

    def post(self, request, format=None):
        serialize = ProductSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            response = methods.getPositiveResponse(f"Product '{serialize.data['name']}' Added Successfully",status.HTTP_201_CREATED,serialize.data)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Product is Not Added ",status.HTTP_400_BAD_REQUEST,serialize.errors)
            return Response(response,status=response['statusCode'])

class ProductDetailsView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get_object(self,pk=None):
        try:
            product = Product.objects.get(pk=pk)
            return product
        except:
            pass

    def get(self,request,pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except:
            response = methods.getNegativeResponse("Product Not Found",status.HTTP_404_NOT_FOUND)
            return Response(response,status=response['statusCode'])
        serialize=ProductSerializer(product)
        response = methods.getPositiveResponse("Products Details",status.HTTP_200_OK,serialize.data)
        return Response(response,status=response['statusCode'])
    
    def put(self,request,pk=None, formate=None):
        product = self.get_object(pk)
        serialize = ProductSerializer(product,data=request.data)
        if product:
            if serialize.is_valid():
                serialize.save()
                response = methods.getPositiveResponse(f"Product '{serialize.data['name']}' Updated Successfully",status.HTTP_200_OK,serialize.data)
                return Response(response,status=response['statusCode'])
            else:
                response = methods.getNegativeResponse("Product Not Updated ",status.HTTP_400_BAD_REQUEST,serialize.errors)
                return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Product Not Found ",status.HTTP_404_NOT_FOUND)
            return Response(response,status=response['statusCode'])
    
    def delete(self,request,pk=None):
        product = self.get_object(pk)
        product.delete()
        response = methods.getPositiveResponse("Product Deleted Successfully",status.HTTP_200_OK)
        return Response(response,status=response['statusCode'])