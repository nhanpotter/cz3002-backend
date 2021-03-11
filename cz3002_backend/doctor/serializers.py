from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from .models import Doctor


class DoctorProfileSerializer(ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Doctor
        fields = ['user', 'working_address']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        # Update Patient model
        instance.working_address = validated_data.get('working_address',
                                                      instance.working_address)
        instance.save()

        # Update User model
        user.username = user_data.get('username', user.username)
        user.phone_number = user_data.get('phone_number', user.phone_number)
        user.birthday = user_data.get('birthday', user.birthday)
        user.save()

        return instance
