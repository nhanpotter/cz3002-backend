from django.urls import path
from rest_framework import views
from .views import (GameTestRetrieveOwnerView, PatientRetrieveListView,TestCreateView, TrailMakingCreateView,PictureObjectMatchCreateView, 
                    GameTestRetrieveOwnerListView, GameTestRetrieveListView, GameTestRetrieveView,PatientRetrieveView)
urlpatterns = [
    path('',PatientRetrieveListView.as_view(),name="patient-list"),
    path('<uid>',PatientRetrieveView.as_view(),name="patient-list"),

    
    path('new-test/',TestCreateView.as_view(),name="new-test"),

    #owner of resource
    path('tests/<tid>/trail-makings/',TrailMakingCreateView.as_view(),name="create-trail-making"),
    path('tests/<tid>/picture-object-matchs/',PictureObjectMatchCreateView.as_view(),name="create-picture-object-match"),

    path('tests/<tid>',GameTestRetrieveOwnerView.as_view(),name="retrieve-test"),
    path('tests/',GameTestRetrieveOwnerListView.as_view(),name="retrieve-test-list"),

    #other people use this to access
    path('<uid>/tests/<tid>',GameTestRetrieveView.as_view(),name="doctor-retrieve-test"),
    path('<uid>/tests/',GameTestRetrieveListView.as_view(),name="doctor-retrieve-test-list"),

]