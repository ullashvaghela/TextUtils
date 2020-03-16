from djongo import models
from django.utils import timezone
from catalog.subcategory.models import Subcategory

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200,help_text="Enter Product Title")
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    price = models.IntegerField(help_text="Enter Product Unit Cost")
    sku = models.CharField(max_length=200,help_text="Enter Product Stock Keeping Unit")
    quantity = models.IntegerField(help_text="Enter Product Quantity")
    description = models.TextField(help_text="Enter Product Description")
    created_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    buffer_quantity = models.IntegerField(help_text="Enter Buffer Stock Quantity")
    image = models.FileField(blank=True)
    
    def __str__(self):
        return self.name