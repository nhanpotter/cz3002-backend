
from django.db.models import fields
from rest_framework.fields import ReadOnlyField
from .models import User
from rest_framework import serializers
#from django.contrib.auth import authenticate
from .emailAuthBackend import EmailAuthBackend
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import Util

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,min_length=3,write_only=True)

    class Meta:
        model=User
        fields=['email','username','password','working_address',"phone_number"]

    def validate(self,attrs):
        email= attrs.get('email','')
        username=attrs.get('username','')

        #check exception below

        return attrs
    
    def create(self, validated_data):
        print(validated_data)
        #also has create which doesnot hash, so check_password alsway false in authentication
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=1024)

    class Meta:
        model=User
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=3, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(password=password,email=email)
        print(email+" "+password)
        print(filtered_user_by_email)
        user = EmailAuthBackend.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid username or password')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.token
        }

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    #field to expose
    class Meta:
        fields=['email']
    
    def validate(self, attrs):
        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=3,write_only=True)
    uidb64 = serializers.CharField( min_length=1,write_only=True)
    token = serializers.CharField( min_length=1,write_only=True)



    #field to expose
    class Meta:
        fields=['password','token','uidb64']
    
    def validate(self, attrs):
        password=attrs.get('password')
        token=attrs.get('token')
        uidb64=attrs.get('uidb64')
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid',401)
            user.set_password(password)
            user.save()
        except Exception:
            raise AuthenticationFailed('The reset link is invalid,401',401)

        return super().validate(attrs)

