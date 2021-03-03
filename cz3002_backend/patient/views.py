from .renderers import ErrorRenderer
from .models import GameTest
from .serializers import GameTestSerializer, PatientSerializer, TrailMakingSerializer, PictureObjectMatchingSerializer
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework import serializers, status
from authentication.models import User
from .models import Patient
# //return patient profile
#     Get api/v1/patient/<id>/

#     Get api/v1//patient/<id>/test  //return all test result
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2MjIwNDUxLCJqdGkiOiI4ZTU2N2YxYmJiYzM0MTg4YmZmYTBmYmE5MWZlOGViYiIsInVzZXJfaWQiOjF9._ve0ESa1WjalkoaWCFIrLielNHh5NcjgZpTvsFfBt8E

'''
to do list
1. get list of patient
2 get  patient profile
x3 doctor access patient test
x4 doctor access patient test list
5 search patient
'''
class PatientRetrieveListView(ListAPIView):
    serializer_class = PatientSerializer
    renderer_classes=(ErrorRenderer,)
    
    def get(self, request):
        # add pagination 
        query_set=self.get_queryset()
        serializer=self.serializer_class(query_set,many=True)
        data=serializer.data
        return JsonResponse({'patients':data},status=status.HTTP_200_OK)
    
    def get_queryset(self):
        return User.objects.filter(groups__name='patient')

class PatientRetrieveView(RetrieveAPIView):
    serializer_class = PatientSerializer
    renderer_classes=(ErrorRenderer,)
    
    def get(self, request,uid):
        # add pagination 
        query_set=self.get_queryset()
        patient=get_object_or_404(query_set,pk=uid)
        serializer=self.serializer_class(patient)
        data=serializer.data
        print(data)
        return JsonResponse(data,status=status.HTTP_200_OK)
    
    def get_queryset(self):
        return User.objects.filter(groups__name='patient')

class TestCreateView(CreateAPIView):
    def post(self,request):
        try:
            user=User.objects.get(id=request.user.id)
            if not user.groups.filter(name='patient').exists():
                return JsonResponse({'error':'User is not a patient'},status=status.HTTP_400_BAD_REQUEST)
            #here should save since patient must have patient object created in register
            patient=Patient.objects.get(user_id=user.id)
            game_test=GameTest.objects.create(patient_id=patient.id)
            return JsonResponse({"user_id":user.id,
                                "user_name":user.username,
                                'patient_id':patient.id,
                                'new_test_id':game_test.id},status=status.HTTP_201_CREATED)

        except User.DoesNotExist or Patient.DoesNotExist:
            return JsonResponse({'error':'Patient doest not exist'},status=status.HTTP_400_BAD_REQUEST)

class TrailMakingCreateView(CreateAPIView):
    serializer_class=TrailMakingSerializer
    renderer_classes=(ErrorRenderer,)
    def post(self, request,tid):        
        serializer=self.serializer_class(data=request.data,context={'user_id':request.user.id,'test_id':tid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=serializer.data
        return JsonResponse(data,status=status.HTTP_201_CREATED)

class PictureObjectMatchCreateView(CreateAPIView):
    serializer_class=PictureObjectMatchingSerializer
    renderer_classes=(ErrorRenderer,)
    def post(self, request, tid):
        serializer=self.serializer_class(data=request.data,context={'user_id': request.user.id,'test_id':tid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=serializer.data
        return JsonResponse(data,status=status.HTTP_201_CREATED)

class GameTestRetrieveOwnerView(RetrieveAPIView):
    serializer_class = GameTestSerializer
    renderer_classes=(ErrorRenderer,)
   
    def get(self, request, tid):
        query_set=self.get_queryset()
        game_test=get_object_or_404(query_set,pk=tid)
        serializer=self.serializer_class(game_test)
        data=serializer.data
        return JsonResponse(data,status=status.HTTP_200_OK)
    
    def get_queryset(self):
        user = self.request.user
        patient=Patient.objects.get(user_id=user.id)
        return patient.gametest_set.all()
    
class GameTestRetrieveOwnerListView(ListAPIView):
    serializer_class = GameTestSerializer
    renderer_classes=(ErrorRenderer,)
    
    def get(self, request):
        query_set=self.get_queryset()
        if not query_set.exists():
            return JsonResponse({'errors':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(query_set,many=True)
        print(serializer.data)
        return JsonResponse({'game_test':serializer.data},status=status.HTTP_200_OK)
    
    def get_queryset(self):
        user = self.request.user
        patient=Patient.objects.get(user_id=user.id)
        return patient.gametest_set.all()



# other 
class GameTestRetrieveView(RetrieveAPIView):
    serializer_class = GameTestSerializer
    renderer_classes=(ErrorRenderer,)
   
    def get(self, request, uid,tid):
        patient=get_object_or_404(Patient,user_id=uid)
        query_set=patient.gametest_set.all()
        game_test=get_object_or_404(query_set,pk=tid)
        serializer=self.serializer_class(game_test)
        data=serializer.data
        return JsonResponse(data,status=status.HTTP_200_OK)
    
class GameTestRetrieveListView(ListAPIView):
    serializer_class = GameTestSerializer
    renderer_classes=(ErrorRenderer,)
    
    def get(self, request, uid):
        patient=get_object_or_404(Patient,user_id=uid)
        query_set=patient.gametest_set.all()
        if not query_set.exists():
            return JsonResponse({'errors':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=self.serializer_class(query_set,many=True)
        data=serializer.data
        return JsonResponse({'game_test':data},status=status.HTTP_200_OK)




