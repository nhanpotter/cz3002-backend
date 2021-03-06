from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from patient.models import Patient
from .serializers import PatientSerializer, UserSerializer


class SearchAPIView(APIView):
    """API View to search patients by name or email
    """

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

    def get(self, request):
        doctor = request.user.doctor
        if not doctor:
            return Response({'errors': 'doctor not exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        patient_qs = doctor.watchlist.order_by('user__username')
        serializer = PatientSerializer(patient_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        doctor = request.user.doctor
        if not doctor:
            return Response({'errors': 'doctor not exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = serializer.validated_data.patient
        doctor.watchlist.add(patient)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        doctor = request.user.doctor
        if not doctor:
            return Response({'errors': 'doctor not exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = serializer.validated_data.patient
        doctor.watchlist.remove(patient)
        return Response(status=status.HTTP_200_OK)
