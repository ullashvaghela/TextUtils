from django.urls import path
from .views import *

urlpatterns = [
    path('list/', ProductView.as_view()),
    path('<int:pk>', ProductDetailsView.as_view()),
    path('add/', ProductView.as_view()),
    path('update/<int:pk>', ProductDetailsView.as_view()),
    path('delete/<int:pk>', ProductDetailsView.as_view()),
    path('search/<str:query>', ProductView.as_view(),name='productsearch'),
]