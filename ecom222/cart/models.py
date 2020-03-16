from djongo import models
from django.utils import timezone
from product.models import Product
from app_user.models import User

# Create your models here.

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="userid",on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    item_quantity = models.PositiveIntegerField(default=1,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id)