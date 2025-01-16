from django.core.management.base import BaseCommand
import random
from crime_app.models import PoliceOfficer, CrimeReport
from django.utils import timezone

def generate_upvotes():
    all_reports = list(CrimeReport.objects.all())
    all_officers = list(PoliceOfficer.objects.all())

    # Ensure that at least 1/3 of the reports get an upvote
    num_reports_to_upvote = max(1, len(all_reports) // 3)
    reports_to_upvote = random.sample(all_reports, k=num_reports_to_upvote)

    for report in reports_to_upvote:
        # Decide how many upvotes for this report
        num_upvotes_for_this_report = random.randint(1, 5)

        for _ in range(num_upvotes_for_this_report):
            officer = random.choice(all_officers)

            # Check how many upvotes they already have
            if len(officer.upvote_details) >= 1000:
                continue  # skip if at 1000

            # Check if officer already upvoted this particular report
            if any(u["crime_report_id"] == report.id for u in officer.upvote_details):
                continue

            # Access Date_Time_OCC from date_info dictionary
            date_time_occ = None
            if report.date_info and "Date_Time_OCC" in report.date_info:
                date_time_occ = report.date_info["Date_Time_OCC"]

            # Create the upvote subdocument with a single date_time_occ
            new_upvote = {
                "crime_report_id": report.id,  # Use `id` instead of `_id`
                "DR_NO": report.DR_NO,
                "Date_Time_OCC": date_time_occ,
                "Crm_Cd": report.crime_info.get("Crm_Cd") if report.crime_info else None,
                "AREA": report.area_info.get("AREA") if report.area_info else None,
                "AREA_NAME": report.area_info.get("AREA_NAME") if report.area_info else None,
                "Weapon_Used_Cd": report.weapon_info.get("Weapon_Used_Cd") if report.weapon_info else None,
                "created_at": timezone.now(),  # Add current timestamp for created_at
            }

            officer.upvote_details.append(new_upvote)
            officer.save()

class Command(BaseCommand):
    help = "Generate upvotes for existing CrimeReport docs"

    def handle(self, *args, **options):
        generate_upvotes()
        self.stdout.write(self.style.SUCCESS("Upvotes generated successfully!"))
