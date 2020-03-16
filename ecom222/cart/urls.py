from django.urls import path
from .views import CartItemList,CartDetails

urlpatterns = [
    path('', CartItemList.as_view()),
    path('<str:clear>', CartItemList.as_view()),
    path('add/', CartItemList.as_view()),
    path('update/', CartItemList.as_view()),
    path('<int:pk>',CartDetails.as_view()),
]