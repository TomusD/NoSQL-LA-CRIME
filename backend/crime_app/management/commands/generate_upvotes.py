from django.core.management.base import BaseCommand
import random
from crime_app.models import PoliceOfficer, CrimeReport
from django.utils import timezone


class Command(BaseCommand):
    help = "Generate upvotes for existing CrimeReport docs"

    # Handler method for generating upvotes
    def handle(self, *args, **options):
        generate_upvotes()
        self.stdout.write(self.style.SUCCESS("Successfully generated upvotes!"))

def generate_upvotes():
    all_reports = list(CrimeReport.objects.all())
    all_officers = list(PoliceOfficer.objects.all())

    # At least 1/3 of the reports get an upvote
    num_reports_to_upvote = len(all_reports) // 3
    reports_to_upvote = random.sample(all_reports, num_reports_to_upvote)

    for report in reports_to_upvote:
        # How many upvotes for this report
        num_upvotes_for_this_report = random.randint(1, 5)

        for _ in range(num_upvotes_for_this_report):
            officer = random.choice(all_officers)

            # Skip if officer already upvoted this report or has 1000 upvotes
            if len(officer.upvote_details) >= 1000:
                continue
            if any(detail["crime_report_id"] == report._id for detail in officer.upvote_details):
                continue

            # Create the upvote subdocument
            new_upvote = {
                "crime_report_id": report._id,
                "DR_NO": report.DR_NO,
                "Date_Time_OCC": report.date_info.get("Date_Time_OCC")if report.date_info else None,
                "Crm_Cd": report.crime_info.get("Crm_Cd")if report.crime_info else None,
                "AREA": report.area_info.get("AREA") if report.area_info else None,
                "AREA_NAME": report.area_info.get("AREA_NAME") if report.area_info else None,
                "Weapon_Used_Cd": report.weapon_info.get("Weapon_Used_Cd") if report.weapon_info else None,
                "created_at": timezone.now()
            }

            officer.upvote_details.append(new_upvote)
            officer.save()
