from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',SignUp.as_view(),name='signup'),
    path('profile/',UserProfile.as_view(),name='userprofile'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('changepassword/',ChangePassword.as_view(),name='changepassword'),
    path('password_reset/',PasswordResetAPIView.as_view(),name='password_change'),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
]