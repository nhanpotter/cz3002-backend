from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from authentication.models import User
from .models import GameTest, TrailMakingTest, PictureObjectMatchingTest
from .models import Patient
from .renderers import ErrorRenderer
from .serializers import GameTestSerializer, PatientSerializer, TrailMakingSerializer, PictureObjectMatchingSerializer, \
    GameTestPostSerializer

# //return patient profile
#     Get api/v1/patient/<id>/

#     Get api/v1//patient/<id>/test  //return all test result

'''
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2MjIwNDUxLCJqdGkiOiI4ZTU2N2YxYmJiYzM0MTg4YmZmYTBmYmE5MWZlOGViYiIsInVzZXJfaWQiOjF9._ve0ESa1WjalkoaWCFIrLielNHh5NcjgZpTvsFfBt8E
to do list
<<<<<<< HEAD

=======
1. get list of patientø
2 get  patient profile
x3 doctor access patient test
x4 doctor access patient test list
>>>>>>> update patient serializer
5 search patient
'''


class PatientRetrieveListView(ListAPIView):
    serializer_class = PatientSerializer
    renderer_classes = (ErrorRenderer,)

    def get(self, request):
        # add pagination 
        query_set = self.get_queryset()
        serializer = self.serializer_class(query_set, many=True)
        data = serializer.data
        return JsonResponse({'patients': data}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Patient.objects.order_by('user__username')


class PatientRetrieveView(RetrieveAPIView):
    serializer_class = PatientSerializer
    renderer_classes = (ErrorRenderer,)

    def get(self, request, uid):
        # add pagination 
        query_set = self.get_queryset()
        patient = get_object_or_404(query_set, user_id=uid)
        serializer = self.serializer_class(patient)
        data = serializer.data
        return JsonResponse(data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Patient.objects.all()


class TestCreateView(CreateAPIView):
    serializer_class = GameTest

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            if not user.groups.filter(name='patient').exists():
                return JsonResponse({'error': 'User is not a patient'}, status=status.HTTP_400_BAD_REQUEST)
            # here should save since patient must have patient object created in register
            patient = Patient.objects.get(user_id=user.id)
            # Assume that a test either have both results or no result, then
            # with logic below, there will always be at most 1 test with no result
            no_result_game = []
            game_test_qs = GameTest.objects.filter(patient=patient)
            for test in game_test_qs:
                # Find test with either no result or only 1 result
                trail_making_exist = TrailMakingTest.objects.filter(game_test=test).exists()
                picture_object_exist = PictureObjectMatchingTest.objects.filter(game_test=test).exists()
                if not trail_making_exist and not picture_object_exist:
                    no_result_game.append(test)

            if len(no_result_game) == 0:
                game_test = GameTest.objects.create(patient_id=patient.id)
            else:
                game_test = no_result_game.pop(0)  # get first test with no result
                for test in no_result_game:  # delete the remaining test with no results
                    test.delete()

            return JsonResponse({"user_id": user.id,
                                 "user_name": user.username,
                                 'patient_id': patient.id,
                                 'new_test_id': game_test.id}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist or Patient.DoesNotExist:
            return JsonResponse({'error': 'Patient doest not exist'}, status=status.HTTP_400_BAD_REQUEST)


class TrailMakingCreateView(CreateAPIView):
    serializer_class = TrailMakingSerializer
    renderer_classes = (ErrorRenderer,)

    def post(self, request, tid):
        serializer = self.serializer_class(data=request.data, context={'user_id': request.user.id, 'test_id': tid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return JsonResponse(data, status=status.HTTP_201_CREATED)


class PictureObjectMatchCreateView(CreateAPIView):
    serializer_class = PictureObjectMatchingSerializer
    renderer_classes = (ErrorRenderer,)

    def post(self, request, tid):
        serializer = self.serializer_class(data=request.data, context={'user_id': request.user.id, 'test_id': tid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return JsonResponse(data, status=status.HTTP_201_CREATED)


class GameTestRetrieveOwnerView(RetrieveAPIView):
    serializer_class = GameTestSerializer
    renderer_classes = (ErrorRenderer,)

    def get(self, request, tid):
        query_set = self.get_queryset()
        game_test = get_object_or_404(query_set, pk=tid)
        serializer = self.serializer_class(game_test)
        data = serializer.data
        return JsonResponse(data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        patient = Patient.objects.get(user_id=user.id)
        return patient.gametest_set.all()


class GameTestRetrieveOwnerListView(ListAPIView):
    serializer_class = GameTestSerializer
    renderer_classes = (ErrorRenderer,)

    def get(self, request):
        query_set = self.get_queryset()
        if not query_set.exists():
            return JsonResponse({'errors': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(query_set, many=True)
        print(serializer.data)
        return JsonResponse({'game_test': serializer.data}, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        patient = Patient.objects.get(user_id=user.id)
        return patient.gametest_set.all()


# other
class GameTestRetrieveView(RetrieveAPIView):
    serializer_class = GameTestSerializer
    renderer_classes = (ErrorRenderer,)

    def get(self, request, uid, tid):
        patient = get_object_or_404(Patient, user_id=uid)
        query_set = patient.gametest_set.all()
        game_test = get_object_or_404(query_set, pk=tid)
        serializer = self.serializer_class(game_test)
        data = serializer.data
        return JsonResponse(data, status=status.HTTP_200_OK)


class GameTestRetrieveListView(ListAPIView):
    serializer_class = GameTestSerializer
    renderer_classes = (ErrorRenderer,)

    def get(self, request, uid):
        patient = get_object_or_404(Patient, user_id=uid)
        query_set = patient.gametest_set.all()
        if not query_set.exists():
            return JsonResponse({'errors': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(query_set, many=True)
        data = serializer.data
        return JsonResponse({'game_test': data}, status=status.HTTP_200_OK)


class GameTestCreateResultsAPIView(CreateAPIView):
    """API view to post results of all games for a test.
    """
    serializer_class = GameTestPostSerializer
    renderer_classes = (ErrorRenderer,)

    def post(self, request, tid):
        serializer = self.serializer_class(data=request.data, context={'user_id': request.user.id, 'test_id': tid})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({}, status=status.HTTP_201_CREATED)
