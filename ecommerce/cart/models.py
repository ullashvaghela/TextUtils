from djongo import models
from account.models import User
from product.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=False,null=False)
    item_quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product.name)