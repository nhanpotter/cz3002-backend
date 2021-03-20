from django.http import response
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json
from authentication.models import User
import datetime
from .models import Patient,GameTest,TrailMakingTest,PictureObjectMatchingTest

# only test correct result
class PatientOwnerTestCase(APITestCase):
    login_url="/api/auth/login" # email, password

    patient_info_url="/api/patients/"
    new_test_id_url="/api/patients/new-test/"
    all_test_result_url="/api/patients/tests/"
    specfic_test_result="/api/patients/tests/{tid}"
    picture_object_match_url="/api/patients/tests/{tid}/picture-object-matchs/"
    trail_making_url="/api/patients/tests/{tid}/trail-makings/"

    login_email="login@example.com"
    login_password="password"

    def setUp(self):
        birthday = datetime.datetime(2021, 3, 17).date()
        self.user = User.objects.create_user(
            username='login', email=self.login_email,
            birthday=birthday, phone_number='123456789', user_role='patient'
        )
        self.user.set_password(self.login_password)
        self.user.save()
        self.patient=Patient.objects.create(user=self.user)
        request_body={
            "email":self.login_email,
            "password":self.login_password
        }
        response=self.client.post(self.login_url, data=request_body, format='json')
        response_body=json.loads(response.content)
        access_token=response_body["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_patient_info(self):
        response=self.client.get(self.patient_info_url, data={}, format='json')
        response_body=json.loads(response.content)
        self.assertEqual(self.login_email,response_body["patients"][0]["user"]["email"])

    def test_new_test_id(self):
        response=self.client.post(self.new_test_id_url, data={}, format='json')
        response_body=json.loads(response.content)
        self.assertEqual(response_body["new_test_id"],1)
        

    def test_create_picture_object_match(self):
        game_test_id=GameTest.objects.create(patient=self.patient).id
        response=self.client.post(self.picture_object_match_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": 20000,
            "date_time_completed": 1616124042
        }, format='json')
        self.assertEqual(status.HTTP_201_CREATED,response.status_code)

    def test_create_picture_object_wrong_test_id(self):
        response=self.client.post(self.picture_object_match_url.format(tid=999), data={
            "score": 19990,
            "errors": 10,
            "time_taken": 20000,
            "date_time_completed": 1616124042
        }, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST,response.status_code)

    def test_create_picture_object_missing_score(self):
        game_test_id=GameTest.objects.create(patient=self.patient).id
        response=self.client.post(self.picture_object_match_url.format(tid=game_test_id), data={
            "errors": 10,
            "time_taken": 20000,
            "date_time_completed": 1616124042
        }, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST,response.status_code)


    def test_create_trail_making(self):
        game_test_id=GameTest.objects.create(patient=self.patient).id
        response=self.client.post(self.trail_making_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": 20000,
            "date_time_completed": 1616124042
        }, format='json')
        self.assertEqual(status.HTTP_201_CREATED,response.status_code)

    def test_create_trail_making_wrong_test_id(self):
        response=self.client.post(self.trail_making_url.format(tid=999), data={
            "score": 19990,
            "errors": 10,
            "time_taken": 20000,
            "date_time_completed": 1616124042
        }, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST,response.status_code)

    def test_create_trail_making_missing_time_taken(self):
        game_test_id=GameTest.objects.create(patient=self.patient).id
        response=self.client.post(self.trail_making_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "date_time_completed": 1616124042
        }, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST,response.status_code)
    
    def test_get_result_by_wrong_test_id(self):
        response=self.client.get(self.specfic_test_result.format(tid=999), data={}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_test_result_by_id_empty_result(self):
        game_test_id=GameTest.objects.create(patient=self.patient).id
        response=self.client.get(self.specfic_test_result.format(tid=game_test_id), data={}, format='json')
        response_body=json.loads(response.content)
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.assertEqual(0,len(response_body["trail_making"]))
        self.assertEqual(0,len(response_body["picture_object_matching"]))

    def test_get_test_result_by_id(self):
        #may be need combine or put in setUp()
        trail_making_time=10000
        picture_object_time=20000
        game_test_id=GameTest.objects.create(patient=self.patient).id
        self.client.post(self.trail_making_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": trail_making_time,
            "date_time_completed": 1616100000
        }, format='json')
        self.client.post(self.picture_object_match_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": picture_object_time,
            "date_time_completed": 1616124042
        }, format='json')
        response=self.client.get(self.specfic_test_result.format(tid=game_test_id), data={}, format='json')
        response_body=json.loads(response.content)

        self.assertEqual(trail_making_time,response_body["trail_making"][0]["time_taken"])
        self.assertEqual(picture_object_time,response_body["picture_object_matching"][0]["time_taken"])
    
    def test_get_all_test_result_empty_result(self):
        response=self.client.get(self.all_test_result_url, data={}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_all_test_result(self):
        trail_making_time=10000
        picture_object_time=20000
        trail_making_time_2=30000
        picture_object_time_2=40000

        game_test_id=GameTest.objects.create(patient=self.patient).id
        self.client.post(self.trail_making_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": trail_making_time,
            "date_time_completed": 1616100000
        }, format='json')
        self.client.post(self.picture_object_match_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": picture_object_time,
            "date_time_completed": 1616124042
        }, format='json')

        game_test_id=GameTest.objects.create(patient=self.patient).id
        self.client.post(self.trail_making_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": trail_making_time_2,
            "date_time_completed": 1616124042
        }, format='json')
        self.client.post(self.picture_object_match_url.format(tid=game_test_id), data={
            "score": 19990,
            "errors": 10,
            "time_taken": picture_object_time_2,
            "date_time_completed": 1616124042
        }, format='json')

        response=self.client.get(self.all_test_result_url, data={}, format='json')
        response_body=json.loads(response.content)

        self.assertEqual(trail_making_time,response_body["game_test"][0]["trail_making"][0]["time_taken"])
        self.assertEqual(picture_object_time,response_body["game_test"][0]["picture_object_matching"][0]["time_taken"])
        self.assertEqual(trail_making_time_2,response_body["game_test"][1]["trail_making"][0]["time_taken"])
        self.assertEqual(picture_object_time_2,response_body["game_test"][1]["picture_object_matching"][0]["time_taken"])

class PatientNotOwnerTestCase(APITestCase):
    patient_info_url="/api/patients/{uid}"
    all_patient_test_result="/api/patients/{uid}/tests/"
    specfic_test_result="/api/patients/{uid}/tests/{tid}"
    login_url="/api/auth/login" # email, password


    trail_making_time=10000
    picture_object_time=20000
    trail_making_time_2=30000
    picture_object_time_2=40000

    patient_email="patient@gmail.com"

    def setUp(self):
        #create patient and add test
        birthday = datetime.datetime(2021, 3, 17).date()
        user = User.objects.create_user(username='patient', email=self.patient_email,birthday=birthday, phone_number='123456789', user_role='patient')
        user.set_password("123")
        user.save()
        self.uid=user.id
        patient=Patient.objects.create(user=user)

        game_test=GameTest.objects.create(patient=patient)
        self.test_id=game_test.id
        TrailMakingTest.objects.create(score=0,errors=0,time_taken=self.trail_making_time,date_time_completed=1616100000,game_test=game_test)
        PictureObjectMatchingTest.objects.create(score=0,errors=0,time_taken=self.picture_object_time,date_time_completed=1616100000,game_test=game_test)
        game_test=GameTest.objects.create(patient=patient)
        TrailMakingTest.objects.create(score=0,errors=0,time_taken=self.trail_making_time_2,date_time_completed=1616100000,game_test=game_test)
        PictureObjectMatchingTest.objects.create(score=0,errors=0,time_taken=self.picture_object_time_2,date_time_completed=1616100000,game_test=game_test)

        #create doctor
        user = User.objects.create_user(
            username='patient', email="doctor@gmail.com",
            birthday=birthday, phone_number='123456789', user_role='doctor'
        )
        user.set_password("123")
        user.save()

        request_body={
            "email":"doctor@gmail.com",
            "password":"123"
        }
        response=self.client.post(self.login_url, data=request_body, format='json')
        response_body=json.loads(response.content)
        access_token=response_body["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_get_patient_info(self):
        response=self.client.get(self.patient_info_url.format(uid=self.uid), data={}, format='json')
        response_body=json.loads(response.content)
        self.assertEqual(self.patient_email,response_body["user"]["email"])

    
    def test_get_patient_all_test_result(self):
        response=self.client.get(self.all_patient_test_result.format(uid=self.uid), data={}, format='json')
        response_body=json.loads(response.content)
        self.assertEqual(self.trail_making_time,response_body["game_test"][0]["trail_making"][0]["time_taken"])
        self.assertEqual(self.picture_object_time,response_body["game_test"][0]["picture_object_matching"][0]["time_taken"])
        self.assertEqual(self.trail_making_time_2,response_body["game_test"][1]["trail_making"][0]["time_taken"])
        self.assertEqual(self.picture_object_time_2,response_body["game_test"][1]["picture_object_matching"][0]["time_taken"])

    def test_get_patient_test_result_by_id(self):
        response=self.client.get(self.specfic_test_result.format(uid=self.uid,tid=self.test_id), data={}, format='json')
        response_body=json.loads(response.content)
        self.assertEqual(self.trail_making_time,response_body["trail_making"][0]["time_taken"])
        self.assertEqual(self.picture_object_time,response_body["picture_object_matching"][0]["time_taken"])
    
    def test_get_wrong_user_id(self):
        response=self.client.get(self.specfic_test_result.format(uid=99,tid=self.test_id), data={}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    
    def test_get_wrong_test_id(self):
        response=self.client.get(self.specfic_test_result.format(uid=99,tid=self.test_id), data={}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class GameTestCreateResultsTestCase(APITestCase):
    endpoint = '/api/patients/tests/{tid}/results/'

    def setUp(self):
        birthday = datetime.datetime(2000, 1, 30).date()
        self.user = User.objects.create_user(
            username='Hello Kurt World', email='helloworld@example.com',
            birthday=birthday, phone_number='123456789', user_role='patient'
        )
        self.patient = Patient.objects.create(user=self.user)

        # Force authentication
        self.client.force_authenticate(user=self.user)

        self.game_test = GameTest.objects.create(patient=self.patient)

    def test_normal(self):
        data = {
            'trail_making': {
                'score': 2,
                'errors': 11,
                'time_taken': 1000,
                'date_time_completed': 2131231212
            },
            'picture_object_matching': {
                'score': 10,
                'errors': 3,
                'time_taken': 2000,
                'date_time_completed': 2131245678
            }
        }

        post_resp = self.client.post(
            self.endpoint.format(tid=self.game_test.id), data=data, format='json')
        self.assertEqual(post_resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(TrailMakingTest.objects.count(), 1)
        trail_making = TrailMakingTest.objects.first()
        self.assertEqual(trail_making.score, 2)
        self.assertEqual(trail_making.errors, 11)
        self.assertEqual(trail_making.time_taken, 1000)
        self.assertEqual(trail_making.date_time_completed, 2131231212)

        self.assertEqual(PictureObjectMatchingTest.objects.count(), 1)
        picture_object = PictureObjectMatchingTest.objects.first()
        self.assertEqual(picture_object.score, 10)
        self.assertEqual(picture_object.errors, 3)
        self.assertEqual(picture_object.time_taken, 2000)
        self.assertEqual(picture_object.date_time_completed, 2131245678)
