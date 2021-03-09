from django.core.management import call_command
from django.test import TestCase

from authentication.models import User
from doctor.models import Doctor
from patient.models import Patient


class CreatePatientCommandTestCase(TestCase):
    def test_normal(self):
        call_command('create_patient', 10)
        self.assertEqual(User.objects.count(), 10)
        self.assertEqual(Patient.objects.count(), 10)


class CreateDoctorCommandTestCase(TestCase):
    def test_normal(self):
        call_command('create_doctor', 5)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(Doctor.objects.count(), 5)
