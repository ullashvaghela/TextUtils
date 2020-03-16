from account.models import User
from .models import Order,Cart,OrderStatus
from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ordered_item = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=300)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=300)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=150)
    zipcode  = serializers.IntegerField()

    def create(self, validated_data):
        item_list = self.context.get('cart')
        total = 0
        for item in item_list:
            total_item_price=item['product_id__price']*item['item_quantity']
            item['item_total']=total_item_price
            total +=total_item_price
        total_amount = {'total': total}
        item_list.append(total_amount)

        user = self.context.get("user")
        name = validated_data['name']
        email = validated_data['email']
        address = validated_data['address']
        city = validated_data['city']
        state = validated_data['state']
        zipcode = validated_data['zipcode']
        order = Order.objects.create(user=user,ordered_item=item_list,name=name,email=email,address=address,city=city,state=state,zipcode=zipcode)
        order.save()
        return order

    
class OrderStatusSerialiser(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(max_length=300)
        
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance