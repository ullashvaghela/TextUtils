from django.contrib import admin
from django.urls import path
from .category.views import *
from .subcategory.views import *

urlpatterns = [
    path('category/<int:pk>', CategoryDetailsView.as_view()),
    path('category/list/',CategoryView.as_view()),
    path('category/add/',CategoryView.as_view()),
    path('category/update/<int:pk>',CategoryDetailsView.as_view()),
    path('category/delete/<int:pk>',CategoryDetailsView.as_view()),
    path('category/search/<str:query>',CategoryView.as_view()),

    path('subcategory/<int:pk>', SubcategoryDetailsView.as_view()),
    path('subcategory/list/',SubcategoryView.as_view()),
    path('subcategory/add/',SubcategoryView.as_view()),
    path('subcategory/update/<int:pk>',SubcategoryDetailsView.as_view()),
    path('subcategory/delete/<int:pk>',SubcategoryDetailsView.as_view()),
    path('subcategory/search/<str:query>',SubcategoryView.as_view()),
]