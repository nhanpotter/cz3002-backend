from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import generic
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework import status

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
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)


class TrailMatchCreateView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

class TrailMatchGetUpdateView(RetrieveUpdateAPIView):
    def get(self, request,id):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

class TrailMatchListView(ListAPIView):
    def get(self,request):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)


class PictureObjectMatchCreateView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

class PictureObjectMatchGetUpdateView(RetrieveUpdateAPIView):
    def get(self, request,id):
        pass
    def patch(self, request, *args, **kwargs):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)

class PictureObjectMatchListView(ListAPIView):
    def get(self,request):
        return JsonResponse({"error":"under developemnt"},status=status.HTTP_400_BAD_REQUEST)


