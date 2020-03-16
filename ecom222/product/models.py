from djongo import models
from django.utils import timezone
from category.models import Subcategory

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,help_text="Enter Product Title")
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    price = models.IntegerField(help_text="Enter Product Unit Cost")
    sku = models.CharField(max_length=200,help_text="Enter Product Stock Keeping Unit")
    quantity = models.IntegerField(help_text="Enter Product Quantity")
    discription = models.TextField(help_text="Enter Product Description")
    created_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    image = models.FileField(blank=True)
    buffer_stoke = models.IntegerField(help_text="Enter Buffer Stock Quantity")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name