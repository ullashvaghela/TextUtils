from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site 
from datetime import datetime
from django.contrib.auth import authenticate
from .models import User,UserProfile,BlackList
from rest_framework import serializers,request,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from base.helper import BaseAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer,UserProfileSerializer,LoginSerializer,UserPasswordUpdateSerializer,PasswordResetSerializer,PasswordResetConfirmSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from .authentication import CustomAuthentication
from rest_framework.parsers import FormParser, JSONParser
from base import methods,utils
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

# Create your views here.

class SignUp(BaseAPIView):
    permission_classes = (AllowAny,)
    
    def post(self,request):
        signup_serializer = UserSerializer(data=request.data)
        if signup_serializer.is_valid():
            signup_serializer.save()
            response = methods.getPositiveResponse("User Created Successfully",status.HTTP_201_CREATED,signup_serializer.data)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Error in User Creation",status.HTTP_400_BAD_REQUEST,signup_serializer.errors)
            return Response(response,status=response['statusCode'])

class UserProfile(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request,format=None):
        #userdetail = User.objects.all()
        userdetail = User.objects.filter(email = request.user.email)
        serialize = UserSerializer(userdetail,many=True)
        response = methods.getPositiveResponse("Profile detail",status.HTTP_200_OK,serialize.data)
        return Response(response,status=response['statusCode'])

    def put(self,request):
        user = User.objects.get(email = request.user.email)
        profile_serializer = UserProfileSerializer(user,data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            response = methods.getPositiveResponse(f"Profile '{request.user.email}' Update Successfully",status.HTTP_202_ACCEPTED,profile_serializer.data)
            return Response(response)
        response = methods.getNegativeResponse("Profile Not Updated",status.HTTP_400_BAD_REQUEST,profile_serializer.errors)
        return Response(response,status=response['statusCode'])

class Login(BaseAPIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            login_data = login_serializer.validated_data
            try:
                user = User.objects.get(email=login_data['email'])
            except:
                response = methods.getNegativeResponse('Email and Password are incorrect',status.HTTP_406_NOT_ACCEPTABLE)
                return Response(response,status=response['statusCode'])
                
            if not user.check_password(login_data['password']):
                response = methods.getNegativeResponse("Email and Password are incorrect",status.HTTP_406_NOT_ACCEPTABLE)
                return Response(response,status=response['statusCode'])
        
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.last_login = datetime.now()
            user.save()
            user_details = {'token':'JWT '+token, 'email':user.email}
            response = methods.getPositiveResponse("Login Successfully",status.HTTP_200_OK,user_details)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Please Enter email and password Both",status.HTTP_400_BAD_REQUEST,login_serializer.errors)
            return Response(response,status=response['statusCode'])

class Logout(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    def post(self,request):
        token = request.META['HTTP_AUTHORIZATION'][4:]
        black_list_token = BlackList(token=token)
        black_list_token.save()
        response = methods.getPositiveResponse("Logged Out Successfully",status.HTTP_200_OK)
        return Response(response,status=response['statusCode'])

class ChangePassword(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication )
    
    def post(self, request): 
        user = self.request.user
        password_serializer = UserPasswordUpdateSerializer(data=request.data)
        if password_serializer.is_valid():
            password_data = password_serializer.validated_data
            if user.check_password(password_data['password']) == True:
                user.set_password(password_data['new_password'])
                user.save()
                response = methods.getPositiveResponse("Password Updated Successfully",status.HTTP_200_OK)
            else:
                response = methods.getNegativeResponse("Old password is not valid.",status.HTTP_406_NOT_ACCEPTABLE)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("Please Enter old & New password Both",status.HTTP_400_BAD_REQUEST,password_serializer.errors)
            return Response(response,status=response['statusCode'])

class PasswordResetAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = PasswordResetSerializer
    def get_user_email(self, email):
        try:
            user_email = User.objects.get(email=email)
        except:
            return None
        return user_email

    def post(self, request):
        user_email = self.get_user_email(request.data.get('email'))
        token_generator = default_token_generator
        if user_email:
            context = {
                'email': user_email,
                'site': get_current_site(request),
                'site_name': getattr(settings, 'SITE_NAME', None),
                'uid': utils.base36encode(user_email.pk),
                'user': user_email,
                'token': token_generator.make_token(user_email)
            }
            subject = render_to_string('password_reset_email_subject.txt', context)
            subject = ''.join(subject.splitlines())
            message = render_to_string('password_reset_email_content.txt', context)
            msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [user_email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            link = f"{get_current_site(request)}/account/reset/{utils.base36encode(user_email.pk)}/{token_generator.make_token(user_email)}"
            response = methods.getPositiveResponse("Password Reset Email Sent Successfully",status.HTTP_200_OK,link)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getNegativeResponse("You Enter Wrong Email Address",status.HTTP_400_BAD_REQUEST)
            return Response(response,status=response['statusCode'])
        

class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):

        serializer = PasswordResetConfirmSerializer(data=request.data,context={
            'uidb64': kwargs['uidb64'],
            'token': kwargs['token']
            })
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')
            user = serializer.user
            user.set_password(new_password)
            user.save()
            response = methods.getPositiveResponse("Password Reset Successfully",status.HTTP_200_OK,serializer.data)
            return Response(response,status=response['statusCode'])
        else:
            response = methods.getPositiveResponse("Wrong Reset Link OR Password Link already Used",status.HTTP_400_BAD_REQUEST,serializer.errors)
            return Response(response,status=response['statusCode'])