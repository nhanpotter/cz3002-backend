from rest_framework import status
from rest_framework.test import APITestCase
import json
from .models import User
import datetime
from patient.models import Patient

# Create your tests here.
class AuthTestCase(APITestCase):
    login_url="/api/auth/login" # email, password
    logout_url="/api/auth/logout/"
    register_url="/api/auth/register" #email,username,password, phone_number, user_role, birthday

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
        Patient.objects.create(user=self.user)
    
    def test_patient_register(self):
        username="patient1"
        request_body={
            "email":"patient1@gmail.com",
            "password":"password",
            "phone_number":"12345678",
            "username":username,
            "user_role":"patient",
            "birthday": "2021-03-17"
        }
        response=self.client.post(self.register_url, data=request_body, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        response_body=json.loads(response.content)
        self.assertEqual(response_body["username"],username)

    def test_patient_register_missing_email(self):
        username="patient1"
        request_body={
            "password":"password",
            "phone_number":"12345678",
            "username":username,
            "user_role":"patient",
            "birthday": "2021-03-17"
        }
        response=self.client.post(self.register_url, data=request_body, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    
    def test_doctor_register(self):
        username="doctor1"
        request_body={
            "email":"doctor1@gmail.com",
            "password":"password",
            "phone_number":"12345678",
            "username":username,
            "user_role":"doctor",
            "birthday": "2021-03-17"
        }
        response=self.client.post(self.register_url, data=request_body, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        response_body=json.loads(response.content)
        self.assertEqual(response_body["username"],username)

    def test_doctor_register_missing_user_role(self):
        username="doctor1"
        request_body={
            "email":"doctor1@gmail.com",
            "password":"password",
            "phone_number":"12345678",
            "username":username,
            "birthday": "2021-03-17"
        }
        response=self.client.post(self.register_url, data=request_body, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
       

    def test_login(self):
        request_body={
            "email":self.login_email,
            "password":self.login_password
        }
        response=self.client.post(self.login_url, data=request_body, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_login_wrong_email(self):
        request_body={
            "email":"aa@bb.com",
            "password":self.login_password
        }
        response=self.client.post(self.login_url, data=request_body, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_no_authorization_token_in_header(self):
        response=self.client.post(self.logout_url, data={"refresh":"123"}, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_logout(self):
        request_body={
            "email":self.login_email,
            "password":self.login_password
        }
        response=self.client.post(self.login_url, data=request_body, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response_body=json.loads(response.content)

        refresh_token=response_body["refresh_token"]
        access_token=response_body["access_token"]
        #it require HTTP_ infront of header key
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response=self.client.post(self.logout_url, data={"refresh":refresh_token}, format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        #response_body=json.loads(response.content)