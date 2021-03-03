from django.urls import path
from rest_framework import views
from .views import (GameTestRetrieveOwnerView, PatientRetrieveListView,TestCreateView, TrailMakingCreateView,PictureObjectMatchCreateView, 
                    GameTestRetrieveOwnerListView, GameTestRetrieveListView, GameTestRetrieveView,PatientRetrieveView)
urlpatterns = [
    path('',PatientRetrieveListView.as_view(),name="patient-list"),
    path('<uid>',PatientRetrieveView.as_view(),name="patient-list"),

    
    path('new-test/',TestCreateView.as_view(),name="new-test"),

    #owner of resource
    path('test/<tid>/trail-making/',TrailMakingCreateView.as_view(),name="create-trail-making"),
    path('test/<tid>/picture-object-match/',PictureObjectMatchCreateView.as_view(),name="create-picture-object-match"),

    path('test/<tid>',GameTestRetrieveOwnerView.as_view(),name="retrieve-test"),
    path('test/',GameTestRetrieveOwnerListView.as_view(),name="retrieve-test-list"),

    #other people use this to access
    path('<uid>/test/<tid>',GameTestRetrieveView.as_view(),name="doctor-retrieve-test"),
    path('<uid>/test/',GameTestRetrieveListView.as_view(),name="doctor-retrieve-test-list"),

]