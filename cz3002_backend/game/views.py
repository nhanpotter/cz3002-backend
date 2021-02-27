from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status
# Create your views here.
def test(request):
    return JsonResponse({"hello":"test"},status=status.HTTP_200_OK)