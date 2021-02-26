
from django.db.models import fields
from .models import User
from rest_framework import serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,min_length=3,write_only=True)

    class Meta:
        model=User
        fields=['email','username','password']

    def validate(self,attrs):
        email= attrs.get('email','')
        username=attrs.get('username','')

        #check exception below


        return attrs
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=1024)

    class Meta:
        model=User
        fields=['token']
