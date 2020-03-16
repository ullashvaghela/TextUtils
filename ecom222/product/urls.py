from django.urls import path
from .views import ProductList,ProductDetails

urlpatterns = [
    path('', ProductList.as_view()),
    path('add/', ProductList.as_view()),
    path('update/<int:pk>', ProductDetails.as_view()),
    path('delete/<int:pk>', ProductDetails.as_view()),
    path('<int:pk>', ProductDetails.as_view()),
    path('search/', ProductList.as_view(),name='productsearch'),
]