from django.urls import path
from rest_framework import views
from .views import GameTestRetrieveView,TestCreateView, PatientProfileView,TrailMakingCreateView,PictureObjectMatchCreateView, GameTestRetrieveListView
urlpatterns = [
    #path('<uid>',PatientProfileView.as_view(),name="user-detail"),
    
    path('new-test',TestCreateView.as_view(),name="new-test"),
    #add tests path to get all test for a user

    #owner of resource
    path('tests/<tid>/trail-making',TrailMakingCreateView.as_view(),name="create-trail-making"),
    path('tests/<tid>/picture-object-match',PictureObjectMatchCreateView.as_view(),name="create-picture-object-match"),
    path('tests/<tid>',GameTestRetrieveView.as_view(),name="get-test"),
    path('tests',GameTestRetrieveListView.as_view(),name="get-test-list"),

    #other people use this to access
    #path('<uid>/test/<tid>/trail-making',TrailMakingCreateView.as_view(),name="create-trail-making"),
    #path('<uid>/test/<tid>/picture-object-match',PictureObjectMatchCreateView.as_view(),name="create-picture-object-match"),


    #path('<uid>/test/<tid>/trail-making/<gid>',TrailMakingGetUpdateView.as_view(),name="read-update-trail-making"),
    #all test for this game for  a user
    #path('<uid>/test/trail-makings',TrailMakingListView.as_view(),name="read-list-trail-making"),
    

    #path('<uid>/test/<tid>/picture-object-match/<gid>',PictureObjectMatchGetUpdateView.as_view(),name="read-update-picture-object-match"),
    #all test for this game for  a user
    #path('<uid>/test/picture-object-matchs',PictureObjectMatchListView.as_view(),name="read-list-picture-object-match"),

]