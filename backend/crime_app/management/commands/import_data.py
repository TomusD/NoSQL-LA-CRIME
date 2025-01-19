import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from crime_app.models import CrimeReport

# Convert value to float, return None if fails
def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

# Command to import data from a CSV
class Command(BaseCommand):
    help = "Import crime data from a CSV file into MongoDB via Django models."

    # Add command line arguments
    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_path',
            type=str,
            required=True,
            help='Path to the CSV file containing crime data.'
        )

    # Handler method to import data from CSV
    def handle(self, *args, **options):
        csv_path = options['csv_path']

        try:
            with open(csv_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                total = 0
                for row in reader:
                    self.insert_report_from_row(row)
                    total += 1
            self.stdout.write(
                self.style.SUCCESS(f"Successfully imported {total} crime reports.")
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error importing data from CSV: {e}")
            )

    # Method to import a single row from the CSV file
    def insert_report_from_row(self, row):
        try:
            # Parsing Date_Rptd
            date_rptd = None
            if row["Date Rptd"].strip():
                try:
                    date_rptd = datetime.strptime(
                        row["Date Rptd"], "%m/%d/%Y %I:%M:%S %p").date()
                except ValueError:
                    self.stderr.write(
                        self.style.WARNING(f"Invalid Date Rptd format: {row['Date Rptd']}")
                    )

            # Date and Time parsing for occurrence
            full_datetime_occ = None
            if row["DATE OCC"].strip():
                try:
                    date_str = row["DATE OCC"].split()[0]
                    date_part = datetime.strptime(date_str, "%m/%d/%Y").date()
                    time_occ = str(row["TIME OCC"]).zfill(4)
                    time_part = datetime.strptime(time_occ, "%H%M").time()
                    full_datetime_occ = datetime.combine(date_part, time_part)
                except ValueError:
                    self.stderr.write(
                        self.style.WARNING(f"Invalid DATE OCC or TIME OCC: {row['DATE OCC']} {row['TIME OCC']}")
                    )

                # Create CrimeReport instance
                crime_report = CrimeReport(
                DR_NO=int(row["DR_NO"]),
                Mocodes=str(row["Mocodes"] or ""),
                date_info={
                    "Date_Rptd": date_rptd.isoformat() if date_rptd else None,
                    "Date_Time_OCC": full_datetime_occ.isoformat() if full_datetime_occ else None,
                },
                area_info={
                    "AREA": int(row["AREA"]),
                    "AREA_NAME": str(row["AREA NAME"] or ""),
                    "Rpt_Dist_No": int(row["Rpt Dist No"]),
                },
                crime_info={
                    "Crm_Cd": int(row["Crm Cd"]),
                    "Crm_Cd_Desc": str(row["Crm Cd Desc"] or ""),
                    "Crime_Codes": [
                        safe_float(row["Crm Cd 1"]),
                        safe_float(row["Crm Cd 2"]),
                        safe_float(row["Crm Cd 3"]),
                        safe_float(row["Crm Cd 4"]),
                    ],
                },
                victim_info={
                    "Vict_Age": int(row["Vict Age"]),
                    "Vict_Sex": str(row["Vict Sex"] or ""),
                    "Vict_Descent": str(row["Vict Descent"] or ""),
                },
                premise_info={
                    "Premis_Cd": safe_float(row["Premis Cd"] or ""),
                    "Premis_Desc": str(row["Premis Desc"] or ""),
                },
                weapon_info={
                    "Weapon_Used_Cd": int(row["Weapon Used Cd"]),
                    "Weapon_Desc": str(row["Weapon Desc"] or ""),
                },
                status_info={
                    "Status": str(row["Status"] or ""),
                    "Status_Desc": str(row["Status Desc"] or ""),
                },
                location_info={
                    "LOCATION": str(row["LOCATION"] or ""),
                    "Cross_Street": str(row["Cross Street"] or ""),
                    "LAT": safe_float(row["LAT"] or ""),
                    "LON": safe_float(row["LON"] or ""),
                },
            )

            crime_report.save()

        except Exception as e:
            self.stderr.write(f"Error processing row: {row}")
            raise
