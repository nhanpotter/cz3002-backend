from .renderers import ErrorRenderer
from .models import GameTest
from .serializers import GameTestSerializer, TrailMakingSerializer, PictureObjectMatchingSerializer
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import generic
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework import serializers, status
from authentication.models import User

# patient
# Get api/v1//patient/test_id
# {
#  	new_test_id: int
# }

# Post api/v1/patient/<id>/test/trail_making
# {
# 	Test ID :
# Score (int):
# Errors (int):
# Time taken to complete (long - milliseconds):
# Date time complete:

# }
# Post api/v1//patient/<id>/test/picture_object_matching
# {
# 	Test ID :
#     Score (int):
#     Errors (int):
#     Time taken to complete (long - milliseconds):
#     Date time complete:
# }

# //return patient profile
#     Get api/v1/patient/<id>/

#     Get api/v1//patient/<id>/test  //return all test result

class PatientProfileView(RetrieveUpdateAPIView):
    
    def get(self, request,id):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

class TestCreateView(CreateAPIView):
    def post(self,request,uid):
        
        try:
            user=User.objects.get(id=uid)
            if not user.groups.filter(name='patient').exists():
                return JsonResponse({'error':'User is not a patient'},status=status.HTTP_400_BAD_REQUEST)
            game_test=GameTest.objects.create(user_id=user.id)
            
            return JsonResponse({"user_id":user.id,
                                "user_name":user.username,
                                'test_id':game_test.id},status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return JsonResponse({'error':'Patient doest not exist'},status=status.HTTP_400_BAD_REQUEST)

    


class TrailMakingCreateView(CreateAPIView):
    serializer_class=TrailMakingSerializer
    renderer_classes=(ErrorRenderer,)
    def post(self, request, uid, tid):
        serializer=self.serializer_class(data=request.data,context={'user_id': uid,'test_id':tid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=serializer.data
        return JsonResponse(data,status=status.HTTP_201_CREATED)

class TrailMakingGetUpdateView(RetrieveUpdateAPIView):
    serializer_class=TrailMakingSerializer

    def get(self, request,id):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

class TrailMakingListView(ListAPIView):
    def get(self,request):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)


class PictureObjectMatchCreateView(CreateAPIView):
    serializer_class=PictureObjectMatchingSerializer
    renderer_classes=(ErrorRenderer,)
    def post(self, request, uid, tid):
        serializer=self.serializer_class(data=request.data,context={'user_id': uid,'test_id':tid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=serializer.data
        return JsonResponse(data,status=status.HTTP_201_CREATED)

class PictureObjectMatchGetUpdateView(RetrieveUpdateAPIView):
    def get(self, request,id):
        pass
    def patch(self, request, *args, **kwargs):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

class PictureObjectMatchListView(ListAPIView):
    def get(self,request):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)


