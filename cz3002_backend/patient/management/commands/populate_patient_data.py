from django.core.management.base import BaseCommand, CommandError
import random
import time
from authentication.models import User
from patient.models import GameTest, TrailMakingTest, PictureObjectMatchingTest


class Command(BaseCommand):
    help = 'Populate test data for one patient'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError('User with email {} not exists'.format(email))

        if not hasattr(user, 'patient'):
            raise CommandError('User is not a patient')

        patient = user.patient
        number_of_test = 10

        current_unix_timestamp_ms = int(time.time() * 1000)
        day_in_ms = 24 * 3600 * 1000
        for _ in range(number_of_test):
            game_test = GameTest.objects.create(patient=patient)
            TrailMakingTest.objects.create(
                game_test=game_test,
                score=random.randint(1, 100),
                errors=random.randint(0, 30),
                time_taken=random.randint(20, 200),
                date_time_completed=current_unix_timestamp_ms
            )
            TrailMakingTest.objects.create(
                game_test=game_test,
                score=random.randint(1, 30),
                errors=random.randint(0, 20),
                time_taken=random.randint(50, 500),
                date_time_completed=current_unix_timestamp_ms
            )
            current_unix_timestamp_ms -= random.randint(15, 30) * day_in_ms

        self.stdout.write(
            self.style.SUCCESS('Successfully create {} game test for user {}'.format(
                number_of_test, email
            ))
        )
