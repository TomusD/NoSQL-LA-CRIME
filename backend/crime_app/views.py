from datetime import datetime
from django.utils.timezone import now
from pymongo import MongoClient
from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import PoliceOfficer, CrimeReport
from crime_app.serializers import (Query1Serializer, Query2Serializer, Query3Serializer,
                                    Query4Serializer, Query5Serializer, Query6Serializer,
                                    Query7Serializer, Query8Serializer, Query9Serializer,
                                    Query10Serializer, PoliceOfficerSerializer, 
                                    CrimeReportSerializer, OfficerUpvoteSerializer
                                )

class query1(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_crimereport']

        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Validate parameters
        if not start_time or not end_time:
            return Response(
                {'error': 'Please provide both starting time and ending time.'},
                status=400
            )

        # Validate time format
        try:
            datetime.strptime(start_time, '%H:%M')
            datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return Response(
                {'error': 'Time format must be HH:MM.'},
                status=400
            )

        # Query 1
        pipeline = [
            {
                "$addFields": {
                    "formatted_time": {
                        "$dateToString": {
                            "format": "%H:%M",
                            "date": {
                                "$dateFromString": {
                                    "dateString": "$date_info.Date_Time_OCC"
                                }
                            }
                        }
                    }
                }
            },
            {
                "$match": {
                    "formatted_time": {"$gte": start_time, "$lte": end_time}
                }
            },
            {
                "$project": {
                    "crime_code": "$crime_info.Crm_Cd"
                }
            },
            {
                "$group": {
                    "_id": "$crime_code",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            },
            {
                "$project": {
                    "Crm_Cd": "$_id",
                    "count": 1,
                    "_id": 0
                }
            }
        ]

        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        
        serializer = Query1Serializer(data, many=True)
        return Response(serializer.data)
    
class query2(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_crimereport']

        start_date = request.query_params.get('start_date')
        start_time = request.query_params.get('start_time')
        end_date = request.query_params.get('end_date')
        end_time = request.query_params.get('end_time')
        crm_cd = request.query_params.get('crm_cd')

        # Validate parameters
        if not start_time or not end_time or not start_date or not end_date or not crm_cd:
            return Response(
                {'error': 'Please provide all parameters.'},
                status=400
            )

        # Validate datetime format and crime code
        try:
            start_datetime = datetime.strptime(f'{start_date} {start_time}', '%Y-%m-%d %H:%M')
            end_datetime   = datetime.strptime(f'{end_date} {end_time}', '%Y-%m-%d %H:%M')
            crm_cd = int(crm_cd)

        except ValueError:
            return Response(
                {'error': 'Date format must be YYYY-MM-DD and time format must be HH:MM.'},
                status=400
            )

        # Query 2
        pipeline = [
            {
                "$addFields": {
                    "formatted_date": {
                        "$dateFromString": {
                            "dateString": "$date_info.Date_Time_OCC"
                        }
                    }
                }
            },
            {
                "$match": {
                    "formatted_date": {
                        "$gte": start_datetime,
                        "$lte": end_datetime
                    },
                    "crime_info.Crm_Cd": crm_cd
                }
            },
            {
                "$group": {
                    "_id": {
                        "date": {
                            "$dateToString": {
                                "format": "%m-%d-%Y",
                                "date": "$formatted_date"
                            }
                        }
                    },
                    "totalReports": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "_id.date": 1
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "date": "$_id.date",
                    "totalReports": 1
                }
            }
        ]

        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        
        serializer = Query2Serializer(data, many=True)
        return Response(serializer.data)

class query3(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_crimereport']

        date = request.query_params.get('date')

        # Validate parameter
        if not date:
            return Response(
                {'error': 'Please provide a date.'},
                status=400
            )
        
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return Response(
                {'error': 'Date format must be YYYY-MM-DD.'},
                status=400
            )

        # Query 3
        pipeline = [
            {
                "$match": {
                    "date_info.Date_Time_OCC": { "$regex": date }
                }
            },
            {
                "$project": {
                    "area_info.AREA": 1,
                    "area_info.AREA_NAME": 1,
                    "crime_codes": {
                        "$filter": {
                            "input": "$crime_info.Crime_Codes",
                            "as": "code",
                            "cond": { "$ne": ["$$code", None] }
                        }
                    }
                }
            },
            {
                "$unwind": "$crime_codes"
            },
            {
                "$group": {
                    "_id": {
                        "area_code": "$area_info.AREA",
                        "area_name": "$area_info.AREA_NAME",
                        "crime_code": "$crime_codes"
                    },
                    "count": { "$sum": 1 }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            },
            {
                "$group": {
                    "_id": {
                        "area_code": "$_id.area_code",
                        "area_name": "$_id.area_name"
                    },
                    "most_common_crimes": {
                        "$push": {
                            "crime_code": "$_id.crime_code",
                            "count": "$count"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "area_code": "$_id.area_code",
                    "area_name": "$_id.area_name",
                    "top_3_crimes": {
                        "$slice": ["$most_common_crimes", 3]
                    }
                }
            }
        ]

        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        
        serializer = Query3Serializer(data, many=True)
        return Response(serializer.data)
    
class query4(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_crimereport']

        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Validate parameters
        if not start_time or not end_time:
            return Response(
                {'error': 'Please provide starting time and ending time.'},
                status=400
            )

        # Validate time format
        try:
            datetime.strptime(start_time, '%H:%M')
            datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return Response(
                {'error': 'Time format must be HH:MM.'},
                status=400
            )

        # Query 4
        pipeline = [
                {
                    "$addFields": {
                        "formatted_time": {
                            "$dateToString": {
                                "format": "%H:%M",
                                "date": {
                                    "$dateFromString": {
                                        "dateString": "$date_info.Date_Time_OCC"
                                    }
                                }
                            }
                        }
                    }
                },
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                {"$gte": ["$formatted_time", start_time]},
                                {"$lte": ["$formatted_time", end_time]}
                            ]
                        }
                    }
                },
                {
                    "$project": {
                        "crime_code": "$crime_info.Crm_Cd"
                    }
                },
                {
                    "$group": {
                        "_id": "$crime_code",
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {
                        "count": 1
                    }
                },
                {
                    "$limit": 2
                },
                {
                    "$project": {
                        "Crm_Cd": "$_id",
                        "count": 1,
                        "_id": 0
                    }
                }
            ]

        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        
        serializer = Query4Serializer(data, many=True)
        return Response(serializer.data)

class query5(APIView):
    def get(self, request):

        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_crimereport']

        # Query 5
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "Crm_Cd": "$crime_info.Crm_Cd",
                        "AREA": "$area_info.AREA"
                    },
                    "Weapon_Types": {
                        "$addToSet": "$weapon_info.Weapon_Desc"
                    }
                }
            },
            {
                "$group": {
                    "_id": "$_id.Crm_Cd",
                    "Areas": {
                        "$addToSet": "$_id.AREA"
                    },
                    "Weapon_Types": {
                        "$addToSet": "$Weapon_Types"
                    }
                }
            },
            {
                "$match": {
                    "Areas.1": {
                        "$exists": True
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "Crm_Cd": "$_id",
                    "Areas": 1,
                    "Weapon_Types": {
                        "$reduce": {
                            "input": "$Weapon_Types",
                            "initialValue": [],
                            "in": {
                                "$setUnion": ["$$value", "$$this"]
                            }
                        }
                    }
                }
            }
        ]


        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )

        serializer = Query5Serializer(data, many=True)
        return Response(serializer.data)

class query6(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_policeofficer']

        date = request.query_params.get('date')

        # Validate parameter
        if not date:
            return Response(
                {'error': 'Please provide a date.'},
                status=400
            )
        
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return Response(
                {'error': 'Date format must be YYYY-MM-DD.'},
                status=400
            )

        # Query 6
        pipeline = [
            {
                "$unwind": "$upvote_details"
            },
            {
                "$match": {
                    "$expr": {
                        "$eq": [
                            {
                                "$dateToString": {
                                    "format": "%Y-%m-%d",
                                    "date": "$upvote_details.Date_Time_OCC"
                                }
                            },
                            date
                        ]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$upvote_details.DR_NO",
                    "upvote_count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "upvote_count": -1
                }
            },
            {
                "$limit": 50
            },
            {
                "$project": {
                    "_id": 0,
                    "DR_NO": "$_id",
                    "upvote_count": 1
                }
            }
        ]

        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )

        serializer = Query6Serializer(data, many=True)
        return Response(serializer.data)

class query7(APIView):
    def get(self, request):

        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_policeofficer']

        # Query 7
        pipeline = [
            {
                "$unwind": "$upvote_details"
            },
            {
                "$group": {
                    "_id": "$badge_number",
                    "officer_name": {"$first": "$name"},
                    "total_upvotes": {"$sum": 1}
                }
            },
            {
                "$sort": {"total_upvotes": -1}
            },
            {
                "$limit": 50
            },
            {
                "$project": {
                    "_id": 0,
                    "badge_number": "$_id",
                    "officer_name": 1,
                    "total_upvotes": 1
                }
            }
        ]


        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        
        serializer = Query7Serializer(data, many=True)
        return Response(serializer.data)

class query8(APIView):
    def get(self, request):

        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_policeofficer']

        # Query 8
        pipeline = [
            {
                "$unwind": "$upvote_details"
            },
            {
                "$group": {
                    "_id": "$badge_number",
                    "officer_name": {
                        "$first": "$name"
                    },
                    "unique_areas": {
                        "$addToSet": "$upvote_details.AREA"
                    }
                }
            },
            {
                "$addFields": {
                    "total_areas": {
                        "$size": "$unique_areas"
                    }
                }
            },
            {
                "$sort": {
                    "total_areas": -1
                }
            },
            {
                "$limit": 50
            },
            {
                "$project": {
                    "_id": 0,
                    "badge_number": "$_id",
                    "officer_name": 1,
                    "total_areas": 1
                }
            }
        ]


        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        
        serializer = Query8Serializer(data, many=True)
        return Response(serializer.data)

class query9(APIView):
    def get(self, request):

        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_policeofficer']

        # Query 9
        pipeline = [
            {
                "$unwind": "$upvote_details"
            },
            {
                "$group": {
                    "_id": {
                        "email": "$email",
                        "DR_NO": "$upvote_details.DR_NO"
                    },
                    "badgeNumbers": {
                        "$addToSet": "$badge_number"
                    }
                }
            },
            {
                "$match": {
                    "$expr": {
                        "$gt": [
                            { "$size": "$badgeNumbers" },
                            1
                        ]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "email": "$_id.email",
                    "DR_NO": "$_id.DR_NO",
                    "badgeNumbers": 1
                }
            }
        ]



        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        
        serializer = Query9Serializer(data, many=True)
        return Response(serializer.data)

class query10(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_policeofficer']

        officer_name = request.query_params.get('officer_name')

        # Validate parameter
        if not officer_name:
            return Response(
                {'error': 'Please provide an officer name.'},
                status=400
            )
        
        # Validate officer name
        try:
            officer_name = str(officer_name)
        except ValueError:
            return Response(
                {'error': 'Officer name must be a string.'},
                status=400
            )

        # Query 10
        pipeline = [
            {
                "$match": {
                    "name": officer_name
                }
            },
            {
                "$unwind": "$upvote_details"
            },
            {
                "$group": {
                    "_id": "$name",
                    "voted_areas": {
                        "$addToSet": {
                            "area_code": "$upvote_details.AREA",
                            "area_name": "$upvote_details.AREA_NAME"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": "$_id",
                    "voted_areas": 1
                }
            }
        ]

        # Execute the query
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )

        serializer = Query10Serializer(data, many=True)
        return Response(serializer.data)
    
class GetCrimeReport(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_crimereport']

        dr_no = request.query_params.get('DR_NO')

        # Validate parameter
        if not dr_no:
            return Response(
                {'error': 'Please provide a Division of Records Number.'},
                status=400
            )
        
        # Validate dr_no
        try:
            dr_no = int(dr_no)
        except ValueError:
            return Response(
                {'error': 'Division of Records Number must be an integer.'},
                status=400
            )

        # Get the crime report
        query = [
            {
                "$match": {
                    "DR_NO": dr_no
                }
            }
        ]

        # Execute the query
        try:
            data = list(collection.aggregate(query))
            if not data:
                return Response(
                    {'message': 'No crime report found with the given Division of Records Number.'},
                    status=404
                )
            
            # Convert ObjectId to string
            for document in data:
                if '_id' in document and isinstance(document['_id'], ObjectId):
                    document['_id'] = str(document['_id'])

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )

        return Response(data)
    
class GetPoliceOfficer(APIView):
    def get(self, request):
        
        # Connect to the database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['LA-CRIME']
        collection = db['crime_app_policeofficer']

        officer_name = request.query_params.get('officer_name')

        # Validate parameter
        if not officer_name:
            return Response(
                {'error': 'Please provide an officer name.'},
                status=400
            )
        
        # Validate officer name
        try:
            officer_name = str(officer_name)
        except ValueError:
            return Response(
                {'error': 'Officer name must be a string.'},
                status=400
            )

        # Get the police officer
        query = [
            {
                "$match": {
                    "name": officer_name
                }
            }
        ]

        # Execute the query
        try:
            data = list(collection.aggregate(query))
            if not data:
                return Response(
                    {'message': 'No officer found with the given name.'},
                    status=404
                )
            
            # Convert ObjectId to string
            for document in data:
                if '_id' in document and isinstance(document['_id'], ObjectId):
                    document['_id'] = str(document['_id'])

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )

        return Response(data)


class AddCrimeReportView(APIView):
    def post(self, request, *args, **kwargs):

        # Validate the data
        serializer = CrimeReportSerializer(data=request.data)

        # Save the data
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Crime report added successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        
        return Response(
            {"message": "Failed to add crime report.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class AddPoliceOfficerView(APIView):
    def post(self, request, *args, **kwargs):

        # Validate the data
        serializer = PoliceOfficerSerializer(data=request.data)

        # Save the data
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Police officer added successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        
        return Response(
            {"message": "Failed to add police officer.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
       )
    
class AddOfficerUpvoteView(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        email = request.data.get("email")
        badge_number = request.data.get("badge_number")
        DR_NO = request.data.get("DR_NO")

        # Validate officer and crime report
        officer = get_object_or_404(PoliceOfficer, name=name, email=email, badge_number=badge_number)
        crime_report = get_object_or_404(CrimeReport, DR_NO=DR_NO)

        # Check if the officer has already upvoted this crime report or has reached the maximum number of upvotes
        if len(officer.upvote_details) >= 1000:
            return Response(
                {"message": "Officer has reached the maximum number of upvotes allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if any(detail["DR_NO"] == DR_NO for detail in officer.upvote_details):
            return Response(
                {"message": "Officer has already upvoted this crime report."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the new upvote
        upvote = {
            "crime_report_id": str(crime_report._id),
            "DR_NO": crime_report.DR_NO,
            "Date_Time_OCC": crime_report.date_info.get("Date_Time_OCC"),
            "Crm_Cd": crime_report.crime_info.get("Crm_Cd"),
            "AREA": crime_report.area_info.get("AREA"),
            "AREA_NAME": crime_report.area_info.get("AREA_NAME"),
            "Weapon_Used_Cd": crime_report.weapon_info.get("Weapon_Used_Cd"),
            "created_at": now()
        }

        # Serialize and validate the data
        upvote_serializer = OfficerUpvoteSerializer(data=upvote)
        upvote_serializer.is_valid(raise_exception=True)

        # Save the upvote
        officer.upvote_details.append(upvote_serializer.validated_data)
        officer.save()

        return Response(
            {"message": "Upvote added successfully!", "upvote_details": upvote_serializer.data},
            status=status.HTTP_201_CREATED,
        )


