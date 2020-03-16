from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token
from .views import SignUp, ProfileUpdate ,UserList,UserDetail,Login, Logout,ChangePassword,ForgotResetPassword

urlpatterns = [
    path('list', UserList.as_view(),name='userlist'),
    path('<int:pk>', UserDetail.as_view(),name='userdetail'),
    path('search/', UserList.as_view(),name='usersearch'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/<int:pk>', ProfileUpdate.as_view(), name='profileupdate'),
    #path('profile/delete/<int:pk>',ProfileUpdate.as_view(), name='profileupdate'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('password', ChangePassword.as_view(), name='changepassword'),
    path('forgot/password', ForgotResetPassword.as_view(), name='ForgotPassword'),
    path('reset/password', ForgotResetPassword.as_view(), name='ResetPassword'),
] 