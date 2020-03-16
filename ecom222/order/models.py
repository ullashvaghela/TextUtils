from djongo import models
from django.utils import timezone
from product.models import Product
from app_user.models import User
from cart.models import CartItem

# Create your models here.

ORDER_STATUS = (
    ("PLACED", "Placed"),
    ("CANCEL", "Cancel"),
)

class OrderStatus(models.Model):
    status = models.CharField(max_length=100,choices=ORDER_STATUS,default="PLACED")

    def __str__(self):
        return self.status

class Order(OrderStatus):
    user = models.ForeignKey(User, related_name="order_user_name",on_delete=models.CASCADE)
    ordered_item = models.TextField()
    name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile_no = models.PositiveIntegerField(default=1,blank=True)
    address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Order ID:"+str(self.id)+"   Order By : "+self.name+"   Email:"+self.user.email+"    Status : "+self.status