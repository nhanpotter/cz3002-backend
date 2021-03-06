from rest_framework.test import APITestCase
from authentication.models import User
from rest_framework import status
from .models import Doctor
from patient.models import Patient


class SearchTestCase(APITestCase):
    endpoint = '/api/doctor/search/'

    def setUp(self):
        self.user = User.objects.create_user(
            username='Nguyen Tien Nhan', email='tiennhan@example.com',
            phone_number='123456789', user_role='doctor'
        )
        Doctor.objects.create(user=self.user)

        # Force authentication
        self.client.force_authenticate(user=self.user)

        # Create patients
        self.user1 = User.objects.create_user(
            username='Hello Kurt World', email='helloworld@example.com',
            phone_number='123456789', user_role='patient'
        )
        Patient.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(
            username='Harry Potter', email='potterhead@example.com',
            phone_number='123456789', user_role='patient'
        )
        Patient.objects.create(user=self.user2)
        self.user3 = User.objects.create_user(
            username='How Are Hello', email='hello@example.com',
            phone_number='123456789', user_role='patient'
        )
        Patient.objects.create(user=self.user3)

    def test_normal(self):
        # List of (query, expected output)
        testcases = [
            (
                {'query': 'hello'},
                [
                    {'user': {
                        'id': self.user1.id,
                        'username': 'Hello Kurt World',
                        'email': 'helloworld@example.com',
                        'phone_number': '123456789'
                    }},
                    {'user': {
                        'id': self.user3.id,
                        'username': 'How Are Hello',
                        'email': 'hello@example.com',
                        'phone_number': '123456789'
                    }}
                ]
            ),
            (
                {'query': 'potterhead@example.com'},
                [
                    {'user': {
                        'id': self.user2.id,
                        'username': 'Harry Potter',
                        'email': 'potterhead@example.com',
                        'phone_number': '123456789'
                    }}
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
        self.user = User.objects.create_user(
            username='Nguyen Tien Nhan', email='tiennhan@example.com',
            phone_number='123456789', user_role='doctor'
        )
        self.doctor = Doctor.objects.create(user=self.user)

        # Force authentication
        self.client.force_authenticate(user=self.user)

        # Create patients
        self.user1 = User.objects.create_user(
            username='Hello Kurt World', email='helloworld@example.com',
            phone_number='123456789', user_role='patient'
        )
        self.patient1 = Patient.objects.create(user=self.user1)
        # Add patient1 to watchlist by default
        self.doctor.watchlist.add(self.patient1)

        self.user2 = User.objects.create_user(
            username='Harry Potter', email='potterhead@example.com',
            phone_number='123456789', user_role='patient'
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
                'phone_number': '123456789'
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
                'phone_number': '123456789'
            }},
            {'user': {
                'id': self.user1.id,
                'username': 'Hello Kurt World',
                'email': 'helloworld@example.com',
                'phone_number': '123456789'
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
