from datetime import datetime
from pymongo import MongoClient
from django.db import connection
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model
from crime_app.serializers import Query1Serializer, Query5Serializer

class query1(APIView):

    def get(self, request):

        
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
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
            start_time_str = start_time_obj.strftime('%H:%M')
            end_time_str = end_time_obj.strftime('%H:%M')
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
                    "formatted_time": {"$gte": start_time_str, "$lte": end_time_str}
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
        # Execute the aggregation pipeline
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        

        serializer = Query1Serializer(data, many=True)
        return Response(serializer.data)
    

class query5(APIView):

    def get(self, request):

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
        # Execute the aggregation pipeline
        try:
            data = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=500
            )
        

        serializer = Query5Serializer(data, many=True)
        return Response(serializer.data)


