from djongo import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name