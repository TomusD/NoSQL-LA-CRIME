from django.core.management.base import BaseCommand
from faker import Faker
from crime_app.models import PoliceOfficer

fake = Faker()

def generate_police_officers(num_officers=50):
    officers = []
    for _ in range(num_officers):
        officer = PoliceOfficer(
            name=fake.name(),
            email=fake.unique.email(),
            badge_number=str(fake.random_number(digits=5)),
        )
        officers.append(officer)
    PoliceOfficer.objects.bulk_create(officers)
    print(f"Successfully created {num_officers} officers!")

class Command(BaseCommand):
    help = "Generate synthetic police officer data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_officers',
            type=int,
            default=50,
            help='Number of police officers to create'
        )

    def handle(self, *args, **options):
        num_officers = options['num_officers']
        generate_police_officers(num_officers=num_officers)
        self.stdout.write(self.style.SUCCESS(
            f"Done generating {num_officers} officers!"
        ))
