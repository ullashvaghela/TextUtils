from django.urls import path
from .views import OrderCheckoutView

urlpatterns = [
    path('list/<int:pk>', OrderCheckoutView.as_view()),
    path('cancle/<int:pk>', OrderCheckoutView.as_view()),
    path('<int:pk>', OrderCheckoutView.as_view()),
]