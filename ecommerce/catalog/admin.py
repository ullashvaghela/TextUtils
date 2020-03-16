from django.contrib import admin
from .category.models import Category
from .subcategory.models import Subcategory

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)