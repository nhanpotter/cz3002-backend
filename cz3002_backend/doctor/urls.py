from django.urls import path
from .views import SearchAPIView, WatchListAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='search'),
    path('watchlist/', WatchListAPIView.as_view(), name='watchlist'),
]
