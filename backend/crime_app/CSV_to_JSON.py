import csv
import json
from bson import ObjectId, json_util
from datetime import datetime

def transform_to_nested(data):
    # Combine DATE_OCC and TIME_OCC into a single datetime object
    time_occ = str(data["TIME OCC"]).zfill(4)
    full_datetime_occ = datetime.strptime(
        f"{data['DATE OCC']} {time_occ}", "%m/%d/%Y %H%M"
    )
    
    return {
        "_id": ObjectId(),
        "DR_NO": int(data["DR_NO"]),
        "Mocodes": data["Mocodes"],

        "date_info": {
            "Date_Rptd": data["Date Rptd"],
            "DATE_OCC": data["DATE OCC"],
            "Date_Time_OCC": full_datetime_occ.isoformat()
        },
        "area_info": {
            "AREA": int(data["AREA"]),
            "AREA_NAME": data["AREA NAME"],
            "Rpt_Dist_No": int(data["Rpt Dist No"])
        },
        "crime_info": {
            "Crm_Cd": int(data["Crm Cd"]),
            "Crm_Cd_Desc": data["Crm Cd Desc"],
            "Crime_Codes": [
                float(data["Crm Cd 1"]) if data["Crm Cd 1"] else None,
                float(data["Crm Cd 2"]) if data["Crm Cd 2"] else None,
                float(data["Crm Cd 3"]) if data["Crm Cd 3"] else None,
                float(data["Crm Cd 4"]) if data["Crm Cd 4"] else None
            ]
        },
        "victim_info": {
            "Vict_Age": int(data["Vict Age"]),
            "Vict_Sex": data["Vict Sex"],
            "Vict_Descent": data["Vict Descent"]
        },
        "premise_info": {
            "Premis_Cd": float(data["Premis Cd"]),
            "Premis_Desc": data["Premis Desc"]
        },
        "weapon_info": {
            "Weapon_Used_Cd": int(data["Weapon Used Cd"]),
            "Weapon_Desc": data["Weapon Desc"]
        },
        "status_info": {
            "Status": data["Status"],
            "Status_Desc": data["Status Desc"]
        },
        "location_info": {
            "LOCATION": data["LOCATION"],
            "Cross_Street": data["Cross Street"],
            "LAT": float(data["LAT"]),
            "LON": float(data["LON"])
        }
    }

# Load the CSV file
csv_file_path = "F:/github/NoSQL-LA-CRIME/first_100_rows.csv" # FIX THIS PATH
nested_data = []

with open(csv_file_path, "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        nested_data.append(transform_to_nested(row))

# Save the nested JSON data
with open("first_100_rows.json", "w") as file: # FIX THIS PATH
    file.write(json_util.dumps(nested_data, indent=4))

print("Data transformation complete. Nested JSON saved.")