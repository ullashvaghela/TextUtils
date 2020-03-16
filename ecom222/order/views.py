from django.shortcuts import render
from django.contrib.auth.models import User

from .models import CartItem,Order,OrderStatus
from cart.serializers import CartItemSerializer
from product.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from .serializers import OrderSerializer,OrderStatusSerialiser
from django.http import Http404


class OrderCheckoutView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,pk, format=None):
        product = Order.objects.filter(user=pk)
        serializer = OrderSerializer(product, many=True)
        return Response(serializer.data)

    def get_object(self,pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Http404
    
    serializer_class = OrderSerializer
    def post(self, request, format=None):
        cart = CartItem.objects.filter(user=request.user.id).values_list('id',flat=True)
        if cart:
            total_amount = 0
            total_quantity = 0
            total_item_list=[]
            for i in cart:
                cart_item = CartItem.objects.get(id=i)
                product_name=cart_item.product.name
                product_price=cart_item.product.price
                product_quantity = cart_item.item_quantity

                item_total_price = product_quantity*product_price
                total_amount += item_total_price 
                total_quantity += product_quantity

                list_of_item = {
                    product_name : {
                        "price" :product_price,
                        "quantity":product_quantity,
                        "item_total_price":item_total_price,
                    }             
                }
                total_item_list.append(list_of_item)
            
            total = {
                "total_quantity":total_quantity,
                "total_amount":total_amount,
            }
            total_item_list.append(total)
            data = {
                "user":self.request.user.id,
                "ordered_item":str(total_item_list),
                "name" : request.data['name'],
                "email" : request.data['email'],
                "mobile_no":request.data['mobile_no'],
                "address":request.data['address'],
                "city":request.data['city'],
                "state":request.data['state'],
                "zipcode":request.data['zipcode'],
            }
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # cart = CartItem.objects.filter(user=request.user.id)
                # cart.delete()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Please Add Some Item In Cart")
    
    def put(self, request,pk, format=None):
        try:
            order_no = Order.objects.get(id=pk)
            print(order_no.status)
            order_no.status=request.data['status']
            order_no.save()
            return Response(f"Your Order No:{pk} is Successfully Cancled")
        except:
            return Response("Your Order is Not Possible To Cancled Out")
            
                 
            # serialize = OrderStatusSerialiser(order_no,data=request.data)
            # #print(serialize.data)
            # if serialize.is_valid():
            #     serialize.save()
            #     return Response(serialize.data)
            # return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
        
    # def delete(self,request,pk):
    #     order_no = Order.objects.filter(user=request.user.id,pk=pk)
    #     print(order_no)
    #     order_no.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)