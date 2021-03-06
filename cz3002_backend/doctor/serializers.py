from rest_framework.serializers import ModelSerializer

from authentication.models import User
from patient.models import Patient


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number']


class PatientSerializer(ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Patient
        fields = ['user']
