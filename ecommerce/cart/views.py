from django.shortcuts import render
from .serializers import CartSerializer
from .models import Cart
from product.models import Product
from base.helper import BaseAPIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from django.http import Http404

from base import methods
# Create your views here.

class CartView(BaseAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            product = Cart.objects.filter(user = self.request.user)
        except:
            None
        serializer = CartSerializer(product, many=True)
        response = methods.getPositiveResponse(f"Cart Item : ",status.HTTP_200_OK,serializer.data)
        return Response(response,status=response['statusCode'])
    
    def post(self, request,pk, format=None):
        try:
            cart = Cart.objects.get(product_id=pk,user = self.request.user)
            serializer = CartSerializer(cart,data=request.data,context = {"product":pk})
            if serializer.is_valid():
                serializer.save()
                response = methods.getPositiveResponse(f"Product Quantity Update Successfully",status.HTTP_200_OK,serializer.data)
                return Response(response,status=response['statusCode'])
            else:
                response = methods.getNegativeResponse("Product is Not Added in the cart",status.HTTP_400_BAD_REQUEST,serializer.errors)
                return Response(response,status=response['statusCode'])
        except Cart.DoesNotExist:
            context = {"user": self.request.user,"product":pk}
            serializer = CartSerializer(data=request.data,context=context)
            if serializer.is_valid():
                serializer.save()
                response = methods.getPositiveResponse(f"Product Added in Cart Successfully",status.HTTP_201_CREATED,serializer.data)
                return Response(response,status=response['statusCode'])
            else:
                response = methods.getNegativeResponse("Product is Not Added in the cart ",status.HTTP_400_BAD_REQUEST,serializer.errors)
                return Response(response,status=response['statusCode'])
    
class CartDetails(BaseAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self,request,pk=None,clear=None):
        if pk:
            try:
                clearitem = Cart.objects.get(product_id=pk,user = self.request.user)
                clearitem.delete()
                response = methods.getPositiveResponse(f"{clearitem} was remove from shopping cart",status.HTTP_200_OK)
                return Response(response,status=response['statusCode'])
            except:
                response = methods.getNegativeResponse("Product Item Not Found ",status.HTTP_400_BAD_REQUEST)
                return Response(response,status=response['statusCode'])
        elif clear=="0":
            clearcart = Cart.objects.filter(user = self.request.user)
            clearcart.delete()
            response = methods.getPositiveResponse(f"Cart clear Successfully",status.HTTP_200_OK)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Product Item Not Found ",status.HTTP_400_BAD_REQUEST)
            return Response(response,status=response['statusCode'])