from django.urls import path
from rest_framework import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import LogoutAPIView, SetNewPasswordView,RegisterView, RequestPasswordResetEmailView, VerifyEmail, LoginAPIView, PasswordTokenCheckView
urlpatterns = [
    path('register',RegisterView.as_view(),name='register'),
    path('login', LoginAPIView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email-verify',VerifyEmail.as_view(),name='email-verify'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),

    #request password reset email
    path('request-reset-email',RequestPasswordResetEmailView.as_view(),name='request-reset-email'),
    #validate reset toen and uidb64
    path('password-reset-token-check/<uidb64>/<token>/',PasswordTokenCheckView.as_view(),name='password-reset-confirm'),
    #reset process
    path('password-reset',SetNewPasswordView.as_view(),name='password-reset'),

]
