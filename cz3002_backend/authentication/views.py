from django.shortcuts import render
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from .serializers import EmailVerificationSerializer, RegisterSerializer
from .models import User
from .utils import Util
import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import bcrypt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer

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
        Util.send_email(data)
        
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