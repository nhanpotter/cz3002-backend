from re import T
from django.shortcuts import render
from rest_framework import status, generics, views, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from .serializers import LogoutSerializer, SetNewPasswordSerializer, EmailVerificationSerializer, RegisterSerializer, LoginSerializer, RequestPasswordResetEmailSerializer
from .models import User
from .utils import Util
import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import bcrypt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .renderers import ErrorRenderer
class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    renderer_classes=(ErrorRenderer,)

    def post(self,request):
        #todo add bcrypt to password
        user = request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()


        user_data=serializer.data

        
        #generate jwt token
        user = User.objects.get(email=user_data['email'])
        token=RefreshToken.for_user(user).access_token

        #send email
        current_site=get_current_site(request).domain
        absurl='http://'+current_site+reverse('email-verify')+'?token='+str(token)
        email_body=email_body = 'Hi '+user.username + ' Use the link below to verify your email \n' + absurl
        data={'to_email':user.email,'subject':'verify your email','body':email_body}
        #Util.send_email(data)
        
        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class=EmailVerificationSerializer

    #allow to manually enter token in api doc
    token_param_config=openapi.Parameter('token',in_=openapi.IN_QUERY,description='enter token',type=openapi.TYPE_STRING)

    #auto in api doc
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token=request.GET.get('token')
        print(token)
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'successful activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({'error':'Activation link Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    #authentication_classes = ()
    #permission_classes = ()
    serializer_class=LoginSerializer
    renderer_classes=(ErrorRenderer,)


    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class=RequestPasswordResetEmailSerializer
    def post(self,request):
        serializer =self.serializer_class(data=request.data)
        email = request.data.get('email', '')

        #serializer.is_valid(raise_exception=True)
        try:
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            #send email
            current_site=get_current_site(request=request).domain
            absurl='http://'+current_site+reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            email_body=email_body = 'Hi '+user.username + '\n Use the link below to reset your password: \n' + absurl
            data={'to_email':user.email,'subject':'Reset your password','body':email_body}
            Util.send_email(data)
            return Response({"success":"We have sent the reset password link to your email"},status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error":"account does not exist"},status=status.HTTP_404_NOT_FOUND)


        

class PasswordTokenCheckView(generics.GenericAPIView):
    #serializer_class = SetNewPasswordSerializer
    def get(self, request, uidb64, token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({"error":"Token is not valid, please request a new one"},status=status.HTTP_401_UNAUTHORIZED)
            return Response({"success":True,
                            'message':'valid token',
                            "uidb64":uidb64,
                            "token":token
                            },status=status.HTTP_200_OK)
            

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({"error":"Token is not valid, please request a new one"},status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success":True,'message':'Password reset success'},status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
