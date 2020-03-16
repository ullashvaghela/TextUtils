from rest_framework import serializers
from .models import User,UserProfile
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from base import utils

class UserProfileSerializer(serializers.Serializer):
    address =  serializers.CharField(max_length=500,required=False)
    city = serializers.CharField(max_length=30,required=False)
    state = serializers.CharField(max_length=30,required=False)
    zipcode = serializers.IntegerField(required=False)
    mobile_number = serializers.IntegerField(required=False) 
    
    def update(self, instance,validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.save()
        instance.profile.address = validated_data.get('address', instance.profile.address)
        instance.profile.city = validated_data.get('city', instance.profile.city)
        instance.profile.state = validated_data.get('state', instance.profile.state)
        instance.profile.zipcode = validated_data.get('zipcode', instance.profile.zipcode)
        instance.profile.mobile_number = validated_data.get('mobile_number', instance.profile.mobile_number)
        instance.profile.save()
        return instance.profile

class UserSerializer(serializers.ModelSerializer):
    
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','profile']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):    
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True,error_messages={'required': 'Please Enter Your Password.'})
    
class UserPasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=5, max_length=35, allow_blank=False, required=True, error_messages={
        'required': 'Please confirm your password.',
        'blank': 'New password may not be blank'
    })
    password = serializers.CharField(min_length=5, max_length=35, allow_blank=False, required=True, error_messages={
        'required': 'Please enter a password.',
        'blank': 'Password may not be blank'
    })

class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):

    token_generator = default_token_generator

    def __init__(self, *args, **kwargs):
        context = kwargs['context']
        uidb64, token = context.get('uidb64'), context.get('token')
        if uidb64 and token:
            uid = utils.base36decode(uidb64)
            self.user = self.get_user(uid)
            self.valid_attempt = self.token_generator.check_token(self.user, token)
        super(PasswordResetConfirmSerializer, self).__init__(*args, **kwargs)

    def get_user(self, uid):
        try:
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    new_password = serializers.CharField(style={'input_type': 'password'},label="New Password",write_only=True)
    new_password_2 = serializers.CharField(style={'input_type': 'password'},label="Confirm New Password",write_only=True)

    def validate_new_password_2(self, value):
        data = self.get_initial()
        new_password = data.get('new_password')
        if new_password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate(self, data):
        if not self.valid_attempt:
            raise serializers.ValidationError("Operation not allowed.")
        return data
        