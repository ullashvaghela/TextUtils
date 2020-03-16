from django.shortcuts import render,get_object_or_404
from .serializers import CartItemSerializer
from product.serializers import ProductSerializer
from .cart import CartObj
from .models import CartItem
from product.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from django.http import Http404

# Create your views here.
class CartItemList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        try:
            product = CartItem.objects.filter(user=request.data['user'])
        except:
            product = CartItem.objects.all()
        serializer = CartItemSerializer(product, many=True)
        return Response(serializer.data)

    def get_object(self,pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Http404

    def post(self, request, format=None):
        try:
            cart = CartItem.objects.get(product=request.data['product'],user=request.data['user'])
            serializer = CartItemSerializer(cart,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,clear):
        if clear=="0":
            print("clear cart : ",clear)
            clearcart = CartItem.objects.filter(user=request.data['user'])
            clearcart.delete()
        else:
            clearitem = CartItem.objects.get(product=request.data['product'],user=request.data['user'])
            clearitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartDetails(APIView):
    permission_classes = (AllowAny,)

    def get_object(self,pk):
        try:
            return CartItem.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Http404

    def get(self,request,pk):
        product = self.get_object(pk)
        serialize=CartItemSerializer(product)
        return Response(serialize.data)