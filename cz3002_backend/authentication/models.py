from django.db import models
# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group


class UserManager(BaseUserManager):

    def create_user(self, username, email, phone_number, user_role, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')
        if phone_number is None:
            raise TypeError('Users should have a phone number')

        user = self.model(username=username, email=self.normalize_email(email),
                          phone_number=phone_number)
        user.set_password(password)

        # Set
        if user_role == 'doctor':
            user.is_staff = True

        # add group
        group = Group.objects.get(name=user_role)
        user.save()
        user.groups.add(group)
        
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    # Note: username is user's real name
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=32, null=False)

    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.USERNAME_FIELD
    USERNAME_FIELD = 'email'
    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        token=RefreshToken.for_user(self)
        return{
            "refresh": str(token),
            "access":str(token.access_token)
        }

