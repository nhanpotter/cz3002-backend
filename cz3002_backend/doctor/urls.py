from django.urls import path

from .views import SearchAPIView, WatchListAPIView, DoctorProfileAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='search'),
    path('watchlist/', WatchListAPIView.as_view(), name='watchlist'),
    path('profile/', DoctorProfileAPIView.as_view(), name='doctor-profile')
]
