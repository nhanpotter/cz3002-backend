from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from patient.models import Patient
from patient.serializers import PatientSerializer

ERROR_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'errors': openapi.Schema(type=openapi.TYPE_STRING, title='error message')
    }
)


class SearchAPIView(APIView):
    """API View to search patients by name or email
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, type=openapi.TYPE_STRING)],
        responses={
            200: PatientSerializer(many=True),
            400: ERROR_SCHEMA
        }
    )
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"errors": "Empty query"},
                            status=status.HTTP_400_BAD_REQUEST)
        patient_qs = Patient.objects.all()
        filter_qs = patient_qs.filter(
            Q(user__username__icontains=query) | Q(user__email__icontains=query))

        serializer = PatientSerializer(filter_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WatchListAPIView(APIView):
    """API View to create, retrieve and delete patients from watchlist
    """

    @swagger_auto_schema(
        responses={
            200: PatientSerializer(many=True),
            400: ERROR_SCHEMA
        }
    )
    def get(self, request):
        doctor = request.user.doctor
        if not doctor:
            return Response({'errors': 'doctor not exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        patient_qs = doctor.watchlist.order_by('user__username')
        serializer = PatientSerializer(patient_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, title='user id')
            }
        ),
        responses={
            200: PatientSerializer(many=True),
            400: ERROR_SCHEMA
        }
    )
    def post(self, request):
        doctor = request.user.doctor
        if not doctor:
            return Response({'errors': 'doctor not exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'id' not in request.data:
            return Response({'errors': 'id not specified'},
                            status=status.HTTP_400_BAD_REQUEST)

        patient_user_id = request.data.get('id')
        try:
            patient = Patient.objects.get(user_id=patient_user_id)
        except Patient.DoesNotExist:
            return Response({'errors': 'patient is not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        doctor.watchlist.add(patient)
        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, title='user id')
            }
        ),
        responses={
            200: PatientSerializer(many=True),
            400: ERROR_SCHEMA
        }
    )
    def delete(self, request):
        doctor = request.user.doctor
        if not doctor:
            return Response({'errors': 'doctor not exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'id' not in request.data:
            return Response({'errors': 'id not specified'},
                            status=status.HTTP_400_BAD_REQUEST)

        patient_user_id = request.data.get('id')
        try:
            patient = Patient.objects.get(user_id=patient_user_id)
        except Patient.DoesNotExist:
            return Response({'errors': 'patient is not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        doctor.watchlist.remove(patient)
        return Response(status=status.HTTP_200_OK)
