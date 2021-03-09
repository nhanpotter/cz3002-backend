
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
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.models import Group
from doctor.models import Doctor
from patient.models import Patient
class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,min_length=3,write_only=True)
    user_role= serializers.CharField(max_length=10,min_length=1,write_only=True)

    class Meta:
        model=User
        fields=['email','username','password','working_address',"phone_number",'user_role']

    def validate(self,attrs):
        email= attrs.get('email','')
        username=attrs.get('username','')
        phone_number=attrs.get('phone_number','')
        if not phone_number.isnumeric():
            raise serializers.ValidationError({'message':'Invalid phone number'})
    
        user_role=attrs.get('user_role','')
        group=Group.objects.filter(name=user_role).first()
        if not group:
            raise serializers.ValidationError({'message':'Invalid user_role'})

        return attrs
    
    def create(self, validated_data):
        #also has create which doesnot hash, so check_password alsway false in authentication
        user=User.objects.create_user(**validated_data)

        #because circular import, the code cant put in model
        if validated_data['user_role'] == 'patient':
            Patient.objects.create(user=user)
        if validated_data['user_role'] == 'doctor':
            Doctor.objects.create(user=user)
        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=1024)

    class Meta:
        model=User
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=3, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    access_token = serializers.CharField(max_length=255, min_length=3, read_only=True)
    refresh_token= serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'access_token','refresh_token']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        #filtered_user_by_email = User.objects.filter(password=password,email=email)
        user = EmailAuthBackend.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid username or password')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        token=user.token()
        return {
            'email': user.email,
            'username': user.username,
            'access_token':token['access'],
            'refresh_token': token['refresh'],      
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

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')