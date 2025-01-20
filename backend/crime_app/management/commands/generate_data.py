from django.core.management.base import BaseCommand
from faker import Faker
from crime_app.models import PoliceOfficer

fake = Faker()

class Command(BaseCommand):
    help = "Generate synthetic police officer data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_officers',
            type=int,
            help='Number of police officers to create'
        )

    # Handler method for generating synthetic data
    def handle(self, *args, **options):
        num_officers = options['num_officers']
        generate_police_officers(num_officers=num_officers)
        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {num_officers} officers!"
            )
        )

# Method to generate synthetic police officer data
def generate_police_officers(num_officers):
    for _ in range(num_officers):
        officer = PoliceOfficer(
            name=fake.name(),
            email=fake.unique.email(),
            badge_number=str(fake.random_number(digits=5))
        )
        officer.save()

