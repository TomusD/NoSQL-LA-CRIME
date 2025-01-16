import csv
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from crime_app.models import CrimeReport

def safe_int(val):
    """
    Return an int if val is not empty and convertible;
    otherwise return 0.
    """
    if val is None or val.strip() == '':
        return 0
    try:
        return int(val)
    except ValueError:
        return 0

def safe_float(val):
    """
    Return a float if val is not empty and convertible;
    otherwise return 0.0.
    """
    if val is None or val.strip() == '':
        return 0.0
    try:
        return float(val)
    except ValueError:
        return 0.0

def safe_str(val):
    """
    Return the string if not empty,
    otherwise an empty string.
    """
    if val is None:
        return ''
    return val.strip()

class Command(BaseCommand):
    help = "Import crime data from a CSV file into MongoDB via Django models."

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_path',
            type=str,
            required=True,
            help='Path to the CSV file containing crime data.'
        )

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
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing data: {e}"))

    def insert_report_from_row(self, row):
        try:
            # 1) Date parsing for Date_Rptd
            date_rptd_py = None
            if row["Date Rptd"].strip():
                try:
                    date_rptd_py = datetime.strptime(
                        row["Date Rptd"], "%m/%d/%Y %I:%M:%S %p"
                    ).date()
                except ValueError:
                    self.stderr.write(
                        self.style.WARNING(f"Invalid Date Rptd format: {row['Date Rptd']}")
                    )

            # 2) Date and Time parsing for Date_Time_OCC
            date_occ_py = None
            full_datetime_occ_py = None
            if row["DATE OCC"].strip():
                try:
                    # Extract date part
                    date_str = row["DATE OCC"].split()[0]  # "03/01/2020"
                    date_part = datetime.strptime(date_str, "%m/%d/%Y").date()

                    # Parse TIME OCC
                    time_occ = str(row["TIME OCC"]).zfill(4)  # Ensure it's 4 digits
                    time_part = datetime.strptime(time_occ, "%H%M").time()  # 21:30

                    # Combine date and time
                    full_datetime_occ_py = datetime.combine(date_part, time_part)
                    date_occ_py = date_part
                except ValueError:
                    self.stderr.write(
                        self.style.WARNING(f"Invalid DATE OCC or TIME OCC: {row['DATE OCC']} {row['TIME OCC']}")
                    )

            # 3) Create CrimeReport instance
                crime_report = CrimeReport(
                DR_NO=safe_int(row["DR_NO"]),
                Mocodes=safe_str(row["Mocodes"]),
                date_info={
                    "Date_Rptd": date_rptd_py.isoformat() if date_rptd_py else None,
                    "DATE_OCC": date_occ_py.isoformat() if date_occ_py else None,
                    "TIME_OCC": safe_int(row["TIME OCC"]),
                    "Date_Time_OCC": full_datetime_occ_py.isoformat() if full_datetime_occ_py else None,
                },
                area_info={
                    "AREA": safe_int(row["AREA"]),
                    "AREA_NAME": safe_str(row["AREA NAME"]),
                    "Rpt_Dist_No": safe_int(row["Rpt Dist No"]),
                },
                crime_info={
                    "Crm_Cd": safe_int(row["Crm Cd"]),
                    "Crm_Cd_Desc": safe_str(row["Crm Cd Desc"]),
                    "Crime_Codes": [
                        safe_float(row["Crm Cd 1"]),
                        safe_float(row["Crm Cd 2"]),
                        safe_float(row["Crm Cd 3"]),
                        safe_float(row["Crm Cd 4"]),
                    ],
                },
                victim_info={
                    "Vict_Age": safe_int(row["Vict Age"]),
                    "Vict_Sex": safe_str(row["Vict Sex"]),
                    "Vict_Descent": safe_str(row["Vict Descent"]),
                },
                premise_info={
                    "Premis_Cd": safe_float(row["Premis Cd"]),
                    "Premis_Desc": safe_str(row["Premis Desc"]),
                },
                weapon_info={
                    "Weapon_Used_Cd": safe_int(row["Weapon Used Cd"]),
                    "Weapon_Desc": safe_str(row["Weapon Desc"]),
                },
                status_info={
                    "Status": safe_str(row["Status"]),
                    "Status_Desc": safe_str(row["Status Desc"]),
                },
                location_info={
                    "LOCATION": safe_str(row["LOCATION"]),
                    "Cross_Street": safe_str(row["Cross Street"]),
                    "LAT": safe_float(row["LAT"]),
                    "LON": safe_float(row["LON"]),
                },
            )

            # 4) Save the CrimeReport instance
            crime_report.save()

        except Exception as e:
            self.stderr.write(f"Error processing row: {row}")
            import traceback
            traceback.print_exc()
            raise e
