from django.urls import path
from .views import *

urlpatterns = [
    path('list/', OrderView.as_view()),
    path('add/', OrderView.as_view()),
    path('update/<int:pk>', OrderStatusView.as_view()),
]