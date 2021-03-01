from django.urls import path
from rest_framework import views
from .views import TrailMatchListView, PictureObjectMatchListView,TestCreateView, PatientProfileView,TrailMatchCreateView,TrailMatchGetUpdateView,PictureObjectMatchCreateView, PictureObjectMatchGetUpdateView
urlpatterns = [
    path('<uid>',PatientProfileView.as_view(),name="user-detail"),
    
    path('<uid>/test',TestCreateView.as_view(),name="newtest"),
    #add tests path to get all test for a user


    path('<uid>/test/<tid>/trail-making',TrailMatchCreateView.as_view(),name="create-trail-making"),
    path('<uid>/test/<tid>/trail-making/<gid>',TrailMatchGetUpdateView.as_view(),name="read-update-trail-making"),
    #all test for this game for  a user
    path('<uid>/test/trail-makings',TrailMatchListView.as_view(),name="read-list-trail-making"),

    path('<uid>/test/<tid>/picture-object-match',PictureObjectMatchCreateView.as_view(),name="create-picture-object-match"),
    path('<uid>/test/<tid>/picture-object-match/<gid>',PictureObjectMatchGetUpdateView.as_view(),name="read-update-picture-object-match"),
    #all test for this game for  a user
    path('<uid>/test/picture-object-matchs',PictureObjectMatchListView.as_view(),name="read-list-picture-object-match"),

]