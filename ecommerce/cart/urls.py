from django.urls import path
from .views import *

urlpatterns = [
    path('list/', CartView.as_view()),
    path('add/<int:pk>', CartView.as_view()),
    path('clearcart/<str:clear>', CartDetails.as_view()),
    path('delete/<int:pk>', CartDetails.as_view()),
]