from django.db.models import Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from patient.models import Patient
from .serializers import PatientSerializer


class SearchAPIView(APIView):
    """API View to search patients by name or email
    """

    def get(self, request: Request):
        query = request.query_params.get('query')
        if not query:
            return Response({"errors": "Empty query"},
                            status=status.HTTP_400_BAD_REQUEST)
        patient_qs = Patient.objects.all()
        filter_qs = patient_qs.filter(
            Q(user__username__icontains=query) | Q(user__email__icontains=query))

        serializer = PatientSerializer(filter_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
