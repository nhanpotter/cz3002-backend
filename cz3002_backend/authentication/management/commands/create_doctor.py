from django.core.management.base import BaseCommand
from faker import Faker

from authentication.models import User
from doctor.models import Doctor


class Command(BaseCommand):
    help = 'Create augmented patient data'

    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        quantity = options['quantity']
        for _ in range(quantity):
            user = User.objects.create_user(
                username=fake.name(), email=fake.email(), phone_number=fake.phone_number(),
                birthday=fake.date_between(start_date='-50y', end_date='-20y'),
                user_role='doctor', password='password'
            )
            Doctor.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS('Successfully create "%s" doctors' % quantity))
