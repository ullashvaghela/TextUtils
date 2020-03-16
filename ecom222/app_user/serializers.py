from rest_framework import serializers
from .models import User,UserVerification
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from datetime import datetime,timedelta
import random, string
from ecom import settings

def randomGeneratorCode(size=25, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
    
class UserSerializar(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email','first_name','last_name','address','city','state','zipcode','contact_number')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
       password = validated_data.pop("password")
       instance.__dict__.update(validated_data)
       if password:
           instance.set_password(password)
       instance.save()
       return instance

class LoginSerializer(serializers.Serializer):    
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(required=True, write_only=True)
    
class UserPasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=5, max_length=35, allow_blank=False, required=True, error_messages={
        'required': 'Please confirm your password.',
        'blank': 'New password may not be blank'
    })
    password = serializers.CharField(min_length=5, max_length=35, allow_blank=False, required=True, error_messages={
        'required': 'Please enter a password.',
        'blank': 'Password may not be blank'
    })

class EmailVerificationSerializer(serializers.Serializer):
    verification_token = serializers.CharField(max_length=255, required=True, error_messages={
        'required': 'Verification token is required',
        'blank': 'Verification token may not be blank'
    })

    class Meta:
        model = UserVerification
        fields = ('verification_token',)

    def update(self, instance, validated_data):
        user_verification = instance
        user_verification.user.is_verified = True
        user_verification.user.save()
        user_verification.save()
        send_mail({'user': user_verification.user})
        return user_verification


class UserVerificationSerializer(serializers.Serializer):
    verification_type = serializers.CharField(required=False)
    verification_token = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    class Meta:
        model = UserVerification
        fields = ('user','verification_type', 'verification_token','user')

    def create(self, validated_data):
        user_verification = None
        verification_type = UserVerification.USER_VERIFICATION_TYPES[0][0]

        if 'verification_type' in validated_data:
            verification_type = validated_data['verification_type']
        user = User.objects.get(id=validated_data['user'])
    
        user_verifications = UserVerification.objects.filter(user=user)
    
        if user_verifications.count() > 0:
            user_verification = user_verifications[0]
            user_verification.verification_token = validated_data['verification_token']
        else:
            user_verification = UserVerification(
                user=user,
                verification_type=verification_type,
                verification_token=validated_data['verification_token']
            )

        user_verification.save()
        return user_verification

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, error_messages={
        'required': 'Please enter a valid email address.',
        'invalid': 'Please enter a valid email address.',
        'blank': 'Email address may not be blank'
    })

    class Meta:
        model = User
        fields = ('email')

    def update(self, instance, validated_data):
        verification_token = ""
                
        is_unique = False
        while is_unique != True:
            verification_token = randomGeneratorCode()
            try:
                UserVerification.objects.get(
                    verification_token=verification_token)
            except UserVerification.DoesNotExist:
                is_unique = True
        try:
            user = User.objects.get(id=validated_data['user'])
            user_verification = UserVerification.objects.filter(user=user)
            user_verification_serializer = UserVerificationSerializer(UserVerification.objects.get(
                user=user,verification_type=UserVerification.USER_VERIFICATION_TYPES[
                    1][0]
            ),
                data={'user': instance.id, 'verification_token': verification_token})
        except:
            data={'user': instance.id,
                'verification_type': UserVerification.USER_VERIFICATION_TYPES[1][0],
                'verification_token': verification_token
                } 
            user_verification_serializer = UserVerificationSerializer(data={'user': instance.id,
                                                                            'verification_type': UserVerification.USER_VERIFICATION_TYPES[1][0],
                                                                            'verification_token': verification_token
                                                                            }
                                                                      )

        user_verification_serializer.is_valid(raise_exception=True)
        user_verification = user_verification_serializer.save()

        from_email = settings.EMAIL_HOST_USER
        to_email = validated_data['email']
        recipient = [to_email]
        send_mail("message",verification_token, from_email,recipient,fail_silently = False)

        return instance

class ResetPasswordSerializer(serializers.Serializer):
    reset_password_token = serializers.CharField(max_length=255, required=True, error_messages={
        'required': 'Please enter a reset password token.',
        'blank': 'Reset password token may not be blank'
    })
    password = serializers.CharField(min_length=5, max_length=35, required=True, error_messages={
        'required': 'Please enter a password.',
        'blank': 'Password may not be blank'
    })

    class Meta:
        model = UserVerification
        fields = ('reset_password_token', 'password')

    def update(self, instance, validated_data):
        user_verification = instance
        user_verification.user.set_password(validated_data['password'])
        user_verification.user.save()
        user_verification.save()
        return user_verification