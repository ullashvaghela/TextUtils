from django.shortcuts import render,get_object_or_404

# User import.
from rest_framework import filters,generics
from .models import User,BlackList,UserVerification
from .serializers import UserSerializar ,LoginSerializer, UserPasswordUpdateSerializer,ForgotPasswordSerializer,ResetPasswordSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from datetime import datetime
from .authentication import CustomAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
import logging,traceback
from djongo.models import Q
from datetime import datetime,timedelta


class SignUp(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializar
    def post(self,request):
        serializer = UserSerializar(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}) 
        else:
            data = {
                "error": True,
                "errors": serializer.errors,          
            }
            return Response(data)

class ProfileUpdate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request,pk,format=None):
        userdetail = User.objects.filter(pk=pk)
        serializer = UserSerializar(userdetail, many=True)
        return Response(serializer.data)

    #serializer_class = UserSerializar
    def put(self,request,pk):
        user = User.objects.get(id=pk)
        print(user)
        serializer = UserSerializar(user, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": serializer.errors, "error": True}) 
        serializer = UserSerializar(user)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        user = get_object_or_404(User, id=pk)
        user.delete()
        return Response({"message": "Deleted"})

class UserList(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    def post(self, request, format=None):
        userlist = User.objects.all()
        serializer = UserSerializar(userlist, many=True)
        return Response(serializer.data)
    
    permission_classes = (AllowAny,)
    serializer_class = UserSerializar
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(Q(username__icontains=query)|Q(email__icontains=query))
        return queryset

class UserDetail(APIView):
    def get(self, request,pk,format=None):
        userdetail = User.objects.filter(pk=pk)
        serializer = UserSerializar(userdetail, many=True)
        return Response(serializer.data)

# class UserSearch(generics.ListAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserSerializar
#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = User.objects.all()
#         username = self.request.query_params.get('username', None)
#         if username is not None:
#             queryset = queryset.filter(username=username)
#         return queryset


class Login(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):

        login_ser = LoginSerializer(data=request.data)
        login_ser.is_valid(raise_exception=True)
        login_data = login_ser.validated_data
        try:
            user = User.objects.get(username=login_data['username'])          
        except:
            raise serializers.ValidationError('Username or password are incorrect')

        if not user.check_password(login_data['password']):
                raise serializers.ValidationError('Username or password are incorrect') 

        #if not user.is_verified:
        #    raise serializers.ValidationError('Please verify your account.')

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        
        user.last_login = datetime.now()
        user.save()

        return Response({'token':'JWT '+token,'id':user.id})

class Logout(APIView):
    authentication_classes = (CustomAuthentication,JSONWebTokenAuthentication)
    def post(self, request):
        token = request.META['HTTP_AUTHORIZATION'][4:]
        black_list_token = BlackList(token=token)
        black_list_token.save()
        return Response({'msg':'User logged out'})

class ChangePassword(APIView):
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication )
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user = self.request.user
        password_ser = UserPasswordUpdateSerializer(data=request.data)
        password_ser.is_valid(raise_exception=True)
        password_data = password_ser.validated_data
        
        if user.check_password(password_data['password']) == True:
            user.set_password(password_data['new_password'])
            user.save()
        else:
            raise serializers.ValidationError('Old password is not valid.')
        return Response(['Password Updated.'])


class EmailConfirmation(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, JSONParser)

    def put(self, request):
        response = {}
        try:
            email_verify_serializer = EmailVerificationSerializer(
                data=request.data)
            if email_verify_serializer.is_valid() == False:
                response = self.getErrorResponse(
                    email_verify_serializer, status.HTTP_400_BAD_REQUEST)
                return Response(response, status=response['statusCode'])

            unique_token = email_verify_serializer.data['verification_token']
            user_id = unique_token.split('_')[1].split('$')[0]
            verification_token = unique_token.split('_')[1].split('$')[1]

            try:
                user_id = encrypt_decrypt.decrypt(
                    encrypt_decrypt.getSecretKey(), user_id, True)
            except:
                raise serializers.ValidationError('Invalid verification token')

            try:
                user_verification = UserVerification.objects.all().filter(
                    verification_token=verification_token,
                    user=user_id,
                    verification_type=UserVerification.USER_VERIFICATION_TYPES[0][0]
                ).get()
            except UserVerification.DoesNotExist:
                raise serializers.ValidationError('Invalid verification token')

            email_verify_serializer = EmailVerificationSerializer(
                user_verification, data=request.data)
            email_verify_serializer.is_valid()
            email_verify_serializer.save()

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user_verification.user)
            token = jwt_encode_handler(payload)

            response_data = {
                'token': 'JWT '+token
            }

            response = helper.getPositiveResponse(
                'User verified successfully', response_data)
        except serializers.ValidationError as exp:
            response = self.getValidationErrorMessage(
                exp.detail, status.HTTP_400_BAD_REQUEST)
        except:
            logging.getLogger(__name__).error(traceback.format_exc())
            response = Response('Invalid verification token', status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response, status=response['statusCode'])

class ForgotResetPassword(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,FormParser, JSONParser)

    def post(self, request):
        forgot_password_ser = ForgotPasswordSerializer(data=request.data)
        print(forgot_password_ser)
        if forgot_password_ser.is_valid() == False:
            return Response("Please Enter Email Address")
        try:
            data = forgot_password_ser.data
            data['email'] = data['email'].lower()
            forgot_password_ser = ForgotPasswordSerializer(
                User.objects.get(email=data['email']), data=data)
            forgot_password_ser.is_valid(raise_exception=True)
            user = forgot_password_ser.save()
            return Response("Reset ID send to Your Email")
        except User.DoesNotExist:
            return Response("User Dose Not Exist")

    def put(self, request):
        reset_password_ser = ResetPasswordSerializer(data=request.data)
        print(request.data['reset_password_token'])
        
        if reset_password_ser.is_valid() == False:
            print(request.data['reset_password_token'])
            return Response("Enter The password")

        try:
            unique_token = reset_password_ser.data['reset_password_token']
        except:
            return Response("Token in Valid")

        try:
            code=UserVerification.objects.all()
            dt_time=datetime.fromisoformat(str(code[0])).replace(tzinfo=None)
            cr_time=datetime.fromisoformat(str(datetime.now()))
            now = datetime.utcnow()
            rounded = dt_time +  timedelta(minutes = 5)
            print(now)
            print(rounded)
            if now<rounded:
                user = UserVerification.objects.get(verification_token=unique_token)
                user_id=user.user_id
                user = User.objects.get(id=user_id)
                user.set_password(reset_password_ser.data['password'])
                user.save()
                return Response("password is update")
            else:
                return Response("Your Token is Expired")
        except UserVerification.DoesNotExist:
            return Response("password is not update")