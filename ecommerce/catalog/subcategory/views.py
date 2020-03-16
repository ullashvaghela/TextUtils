from django.shortcuts import render
from djongo.models import Q
from .models import Subcategory,Category
from catalog.subcategory.serializers import SubcategorySerializer
from account.models import User

from django.http import Http404
from base.helper import BaseAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from django.core.exceptions import ObjectDoesNotExist

from base import methods

class SubcategoryView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubcategorySerializer 
    
    def get(self,request,query=None):
        if query:
            subcategory = Subcategory.objects.filter(Q(name__icontains=query))
        else:
            subcategory = Subcategory.objects.all()
        serialize=SubcategorySerializer(subcategory,many=True)
        response = methods.getPositiveResponse("List of Subcategories",status.HTTP_200_OK,serialize.data)
        return Response(response,status=response['statusCode'])

    def post(self, request, format=None):
        serialize = SubcategorySerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            response = methods.getPositiveResponse("Subcategory Added Successfully",status.HTTP_201_CREATED,serialize.data)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Subcategory Not Added ",status.HTTP_400_BAD_REQUEST,serialize.errors)
            return Response(response,status=response['statusCode'])
        
class SubcategoryDetailsView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubcategorySerializer
    
    def get_object(self,pk):
        try:
            return Subcategory.objects.get(pk=pk)
        except Subcategory.DoesNotExist:
            None

    def get(self,request,pk=None):
        try:
            subcategory = Subcategory.objects.get(pk=pk)
        except:
            response = methods.getNegativeResponse("Subcategory Not Found",status.HTTP_404_NOT_FOUND)
            return Response(response)
        serialize=SubcategorySerializer(subcategory)
        response = methods.getPositiveResponse("Subcategory Details",status.HTTP_200_OK,serialize.data)
        return Response(response,status=response['statusCode'])

    def put(self,request,pk, formate=None):
        subcategory = self.get_object(pk)
        serialize = SubcategorySerializer(subcategory,data=request.data)
        if subcategory:
            if serialize.is_valid():
                serialize.save()
                response = methods.getPositiveResponse("Subcategory Updated Successfully",status.HTTP_202_ACCEPTED,serialize.data)
                return Response(response,status=response['statusCode'])
            else:
                response = methods.getNegativeResponse("Subcategory Not Updated ",status.HTTP_400_BAD_REQUEST,serialize.errors)
                return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Subcategory Not Found ",status.HTTP_404_NOT_FOUND)
            return Response(response,status=response['statusCode'])

    def delete(self,request,pk):
        subcategory = self.get_object(pk)
        if subcategory:
            subcategory.delete()
            response = methods.getPositiveResponse("Subcategory Deleted Successfully",status.HTTP_200_OK)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Subcategory Not Found ",status.HTTP_404_NOT_FOUND)
            return Response(response,status=response['statusCode'])
