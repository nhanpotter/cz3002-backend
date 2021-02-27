from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from .models import User

# not using
class EmailAuthBackend(ModelBackend):

    def authenticate( request=None, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        print("===="+ email)
        try:
            user = User.objects.get(email=email)
            if check_password(password,user.password) is True:
                print("pass word check")
                return user
            else:
                print(password)
                print(user.password)
        except User.DoesNotExist:
            pass