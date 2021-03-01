from django.db import models
from django.db.models import fields
from .models import GameTest, PictureObjectMatchingTest, TrailMakingTest
from rest_framework import serializers

class GameTestSerializer(serializers.ModelSerializer):
    class Meta:
        model=GameTest
        fields=['id']
    
    def validate(self,attrs):
        print(attrs)
       
        return attrs
    
    def create(self, validated_data):
        #also has create which doesnot hash, so check_password alsway false in authentication
        return GameTest.objects.create(**validated_data)


class TrailMakingSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrailMakingTest
        fields=['']

    
    def validate(self,attrs):
        print(attrs)
       
        return attrs
    
    def create(self, validated_data):
        pass
