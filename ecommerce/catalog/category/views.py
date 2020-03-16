from django.shortcuts import render
from djongo.models import Q
from .models import Category
from catalog.category.serializers import CategorySerializer
from account.models import User

from django.http import Http404
from base.helper import BaseAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser

from base import methods

class CategoryView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get(self,request,query=None):
        if query:
            category = Category.objects.filter(Q(name__icontains=query))
        else:
            category = Category.objects.all()
        serialize=CategorySerializer(category,many=True)
        response = methods.getPositiveResponse("List of Categories",status.HTTP_200_OK,serialize.data)
        return Response(response,status=response['statusCode'])

    def post(self, request, format=None):
        serialize = CategorySerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            response = methods.getPositiveResponse("Category Added Successfully",status.HTTP_201_CREATED,serialize.data)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Category Not Added ",status.HTTP_400_BAD_REQUEST,serialize.errors)
            return Response(response,status=response['statusCode'])
        

class CategoryDetailsView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            None
            
    def get(self,request,pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except:
            response = methods.getNegativeResponse("Category Not Found",status.HTTP_404_NOT_FOUND)
            return Response(response,status=response['statusCode'])
        serialize=CategorySerializer(category)
        response = methods.getPositiveResponse("Category Details",status.HTTP_200_OK,serialize.data)
        return Response(response,status=response['statusCode'])
    
    def put(self,request,pk, formate=None):
        category = self.get_object(pk)
        serialize = CategorySerializer(category,data=request.data)
        if category:
            if serialize.is_valid():
                serialize.save()
                response = methods.getPositiveResponse("Category Updated Successfully",status.HTTP_202_ACCEPTED,serialize.data)
                return Response(response,status=response['statusCode'])
            else:
                response = methods.getNegativeResponse("Category Not Updated ",status.HTTP_400_BAD_REQUEST,serialize.errors)
                return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Category Not Found ",status.HTTP_400_BAD_REQUEST)
            return Response(response,status=response['statusCode'])

    def delete(self,request,pk):
        category = self.get_object(pk)
        if category:
            category.delete()
            response = methods.getPositiveResponse("Category Deleted Successfully",status.HTTP_200_OK)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Category Not Found ",status.HTTP_400_BAD_REQUEST)
            return Response(response,status=response['statusCode'])
    
    