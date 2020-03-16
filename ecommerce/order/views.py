from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Cart,Order,OrderStatus
from cart.serializers import CartSerializer
from product.models import Product
from base.helper import BaseAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from .serializers import OrderSerializer,OrderStatusSerialiser
from django.http import Http404

from base import methods

# Create your views here.

class OrderView(BaseAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer 

    def get(self, request, format=None):
        order = Order.objects.filter(user=request.user)
        if order:
            serializer = OrderSerializer(order, many=True)
            response = methods.getPositiveResponse(f"Ordered List",status.HTTP_200_OK,serializer.data)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Order List Empty. Please Order Some Item",status.HTTP_400_BAD_REQUEST)
            return Response(response,status=response['statusCode'])

    def post(self,request):
        cart = Cart.objects.filter(user=request.user).values('product_id','product_id__name','product_id__price','item_quantity')
        if cart:
            context = {"user": self.request.user,'cart':list(cart)}
            serializer = OrderSerializer(data=request.data,context=context)
            if serializer.is_valid():
                serializer.save()
                cart = Cart.objects.filter(user=self.request.user)
                cart.delete()
                response = methods.getPositiveResponse(f"Order have been Placed Successfully",status.HTTP_201_CREATED,serializer.data)
                return Response(response,status=response['statusCode'])
            else:
                response = methods.getNegativeResponse("Order Fail ",status.HTTP_400_BAD_REQUEST,serializer.errors)
                return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse('Please Add Some Item Before Place Order',status.HTTP_400_BAD_REQUEST)
            return Response(response,status=response['statusCode'])

class OrderStatusView(BaseAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderStatusSerialiser

    def put(self, request,pk=None, format=None):
        try:
            order_no = OrderStatus.objects.get(id=pk)
            serializer = OrderStatusSerialiser(order_no,data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = methods.getPositiveResponse(f"Your Order No:{pk} is Successfully Cancled",status.HTTP_200_OK,serializer.data)
                return Response(response,status=response['statusCode'])
            else:
                response = methods.getNegativeResponse("Your Order is Not Possible To Cancled Out",status.HTTP_400_BAD_REQUEST,serializer.errors)
                return Response(response,status=response['statusCode'])
        except:
            response = methods.getNegativeResponse("Order Not Found",status.HTTP_400_BAD_REQUEST)
            return Response(response,status=response['statusCode'])
