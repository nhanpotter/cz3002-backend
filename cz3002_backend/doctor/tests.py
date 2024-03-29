from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from patient.models import Patient
from .models import Doctor
import datetime


class SearchTestCase(APITestCase):
    endpoint = '/api/doctor/search/'

    def setUp(self):
        birthday = datetime.datetime(2000, 1, 30).date()
        self.user = User.objects.create_user(
            username='Nguyen Tien Nhan', email='tiennhan@example.com',
            birthday=birthday, phone_number='123456789', user_role='doctor'
        )
        doctor = Doctor.objects.create(user=self.user)

        # Force authentication
        self.client.force_authenticate(user=self.user)

        # Create patients
        self.user1 = User.objects.create_user(
            username='Hello Kurt World', email='helloworld@example.com',
            birthday=birthday, phone_number='123456789', user_role='patient'
        )
        patient1 = Patient.objects.create(user=self.user1)
        # Add patient1 to doctor watchlist
        doctor.watchlist.add(patient1)
        self.user2 = User.objects.create_user(
            username='Harry Potter', email='potterhead@example.com',
            birthday=birthday, phone_number='123456789', user_role='patient'
        )
        Patient.objects.create(user=self.user2)
        self.user3 = User.objects.create_user(
            username='How Are Hello', email='hello@example.com',
            birthday=birthday, phone_number='123456789', user_role='patient'
        )
        Patient.objects.create(user=self.user3)

    def test_normal(self):
        # List of (query, expected output)
        testcases = [
            (
                {'query': 'hello'},
                [
                    {
                        'user': {
                            'id': self.user1.id,
                            'username': 'Hello Kurt World',
                            'email': 'helloworld@example.com',
                            'phone_number': '123456789',
                            'birthday': '2000-01-30'
                        },
                        'added_to_watchlist': True
                    },
                    {
                        'user': {
                            'id': self.user3.id,
                            'username': 'How Are Hello',
                            'email': 'hello@example.com',
                            'phone_number': '123456789',
                            'birthday': '2000-01-30'
                        },
                        'added_to_watchlist': False
                    }
                ]
            ),
            (
                {'query': 'potterhead@example.com'},
                [
                    {
                        'user': {
                            'id': self.user2.id,
                            'username': 'Harry Potter',
                            'email': 'potterhead@example.com',
                            'phone_number': '123456789',
                            'birthday': '2000-01-30'
                        },
                        'added_to_watchlist': False
                    }
                ]
            )
        ]
        for query, expected in testcases:
            response = self.client.get(self.endpoint, data=query, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, expected)

    def test_empty_query_string(self):
        response = self.client.get(self.endpoint, data={'query': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"errors": "Empty query"})

    def test_no_get_params(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"errors": "Empty query"})


class WatchListTestCase(APITestCase):
    endpoint = '/api/doctor/watchlist/'

    def setUp(self):
        birthday = datetime.datetime(2000, 1, 30).date()
        self.user = User.objects.create_user(
            username='Nguyen Tien Nhan', email='tiennhan@example.com',
            birthday=birthday, phone_number='123456789', user_role='doctor'
        )
        self.doctor = Doctor.objects.create(user=self.user)

        # Force authentication
        self.client.force_authenticate(user=self.user)

        # Create patients
        self.user1 = User.objects.create_user(
            username='Hello Kurt World', email='helloworld@example.com',
            birthday=birthday, phone_number='123456789', user_role='patient'
        )
        self.patient1 = Patient.objects.create(user=self.user1)
        # Add patient1 to watchlist by default
        self.doctor.watchlist.add(self.patient1)

        self.user2 = User.objects.create_user(
            username='Harry Potter', email='potterhead@example.com',
            birthday=birthday, phone_number='123456789', user_role='patient'
        )
        self.patient2 = Patient.objects.create(user=self.user2)

    def test_get(self):
        """Test get patient 1 from watchlist
        """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'user': {
                'id': self.user1.id,
                'username': 'Hello Kurt World',
                'email': 'helloworld@example.com',
                'phone_number': '123456789',
                'birthday': '2000-01-30'
            }}
        ])

    def test_post(self):
        """Test add patient 2 to watchlist
        """
        data = {
            'id': self.user2.id
        }
        response = self.client.post(self.endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(self.endpoint)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data, [
            {'user': {
                'id': self.user2.id,
                'username': 'Harry Potter',
                'email': 'potterhead@example.com',
                'phone_number': '123456789',
                'birthday': '2000-01-30'
            }},
            {'user': {
                'id': self.user1.id,
                'username': 'Hello Kurt World',
                'email': 'helloworld@example.com',
                'phone_number': '123456789',
                'birthday': '2000-01-30'
            }}
        ])

    def test_post_id_not_exist(self):
        data = {
            'id': 1000000
        }
        response = self.client.post(self.endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        data = {
            'id': self.user1.id
        }
        response = self.client.delete(self.endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        get_response = self.client.get(self.endpoint)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data, [])

    def test_delete_id_not_exist(self):
        data = {
            'id': 10000000
        }
        response = self.client.delete(self.endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DoctorProfileTestCase(APITestCase):
    endpoint = '/api/doctor/profile/'

    def setUp(self):
        birthday = datetime.datetime(2000, 1, 30).date()
        self.user = User.objects.create_user(
            username='Nguyen Tien Nhan', email='tiennhan@example.com',
            birthday=birthday, phone_number='123456789', user_role='doctor'
        )
        self.doctor = Doctor.objects.create(user=self.user, working_address='NTU')

        # Force authentication
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'user': {
                'id': self.user.id,
                'username': 'Nguyen Tien Nhan',
                'email': 'tiennhan@example.com',
                'phone_number': '123456789',
                'birthday': '2000-01-30'
            },
            'working_address': 'NTU'
        })

    def test_post_normal(self):
        data = {
            'user': {
                'username': 'Awesome Nhan',
                'phone_number': '12345678910',
                'birthday': '2000-02-01'
            },
            'working_address': 'NUS'
        }
        response = self.client.post(self.endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, 'Awesome Nhan')
        self.assertEqual(self.user.phone_number, '12345678910')
        self.assertEqual(self.user.birthday, datetime.datetime(2000, 2, 1).date())
        self.assertEqual(self.doctor.working_address, 'NUS')

    def test_post_omit_fields(self):
        testcases = [
            {
                'user': {
                    'username': 'Awesome Nhan'
                },
            },
            {
                'working_address': 'NUS'
            }
        ]
        for data in testcases:
            response = self.client.post(self.endpoint, data=data, format='json')
            self.assertEqual(response.status_code, 400)
