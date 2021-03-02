from django.db import models
from django.db.models import fields
from rest_framework.fields import IntegerField, ReadOnlyField
from .models import GameTest, Patient, PictureObjectMatchingTest, TrailMakingTest
from rest_framework import serializers
from authentication.models import User



class TrailMakingSerializer(serializers.ModelSerializer):
    game_test_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=TrailMakingTest
        fields=['id','score','errors','time_taken','date_time_completed','game_test_id']
    def validate(self,attrs):
        try:
            user_id=self.context.get("user_id")
            user=User.objects.get(id=user_id)
            if not user.groups.filter(name='patient').exists():
                raise serializers.ValidationError("The user is not a patient")

            #here should save since patient must have patient object created in register
            patient=Patient.objects.get(user_id=user.id)

            test_id=self.context.get("test_id")
            game_test=GameTest.objects.get(id=test_id,patient_id=patient.id)
            
            if len(TrailMakingTest.objects.filter(game_test_id=test_id))!=0:
                raise serializers.ValidationError("Trail making test already exist")
            
        except User.DoesNotExist:
            raise serializers.ValidationError("Patient not exist")
        except GameTest.DoesNotExist:
            raise serializers.ValidationError("Invalid test id, please create a new test using /patient/{uid}/test")
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not exist")

        return attrs
    
    def create(self, validated_data):
        #because already validat on top
        test_id=self.context.get("test_id")

        validated_data['game_test_id']=test_id
        return TrailMakingTest.objects.create(**validated_data)

class PictureObjectMatchingSerializer(serializers.ModelSerializer):
    game_test_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=PictureObjectMatchingTest
        fields=['id','score','errors','time_taken','date_time_completed','game_test_id']

    
    def validate(self,attrs):
        try:
            user_id=self.context.get("user_id")
            user=User.objects.get(id=user_id)
            if not user.groups.filter(name='patient').exists():
                raise serializers.ValidationError("The user is not a patient")
            patient=Patient.objects.get(user_id=user.id)          
            test_id=self.context.get("test_id")
            game_test=GameTest.objects.get(id=test_id,patient_id=patient.id)
            if len(PictureObjectMatchingTest.objects.filter(game_test_id=test_id))!=0:
                raise serializers.ValidationError("Trail making test already exist")
            
        except User.DoesNotExist:
            raise serializers.ValidationError("Patient not exist")
        except GameTest.DoesNotExist:
            raise serializers.ValidationError("Invalid test id, please create a new test using /patient/{uid}/test")
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not exist")
        return attrs
    
    def create(self, validated_data):
        #because already validat on top
        test_id=self.context.get("test_id")
        validated_data['game_test_id']=test_id
        return PictureObjectMatchingTest.objects.create(**validated_data)

class GameTestSerializer(serializers.ModelSerializer):
    trail_making = TrailMakingSerializer(many=True,read_only=True,source='trailmakingtest_set')
    picture_object_matching = PictureObjectMatchingSerializer(many=True,read_only=True,source='pictureobjectmatchingtest_set')
    
    class Meta:
        model=GameTest
        fields=['id','patient_id','trail_making','picture_object_matching']
        
    def validate(self,attrs):
        pass
    def get_trail_making(self,game_test):
        trail_making_test=TrailMakingTest.objects.filter(game_test_id=game_test.id).first()
        return TrailMakingSerializer(many=True,read_only=True,source='trailmakingtest_set')