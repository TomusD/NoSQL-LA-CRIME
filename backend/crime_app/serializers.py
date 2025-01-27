from rest_framework import serializers
from crime_app.models import CrimeReport, PoliceOfficer

class CrimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = '__all__'

class OfficerUpvoteSerializer(serializers.Serializer):
    crime_report_id = serializers.CharField(max_length=24)
    DR_NO = serializers.IntegerField()
    Date_Time_OCC = serializers.DateTimeField()
    Crm_Cd = serializers.IntegerField()
    AREA = serializers.IntegerField()
    AREA_NAME = serializers.CharField(max_length=100)
    Weapon_Used_Cd = serializers.IntegerField()
    created_at = serializers.DateTimeField(required=False)


class PoliceOfficerSerializer(serializers.ModelSerializer):
    upvote_details = OfficerUpvoteSerializer(many=True, required=False)

    class Meta:
        model = PoliceOfficer
        fields = '__all__'

class Query1Serializer(serializers.Serializer):
    count = serializers.IntegerField()
    Crm_Cd = serializers.IntegerField()

class Query2Serializer(serializers.Serializer):
    totalReports = serializers.IntegerField()
    date = serializers.CharField()

class Query3Serializer(serializers.Serializer):
    area_code = serializers.IntegerField()
    area_name = serializers.CharField()
    top_3_crimes = serializers.ListField(child=serializers.CharField())

class Query4Serializer(serializers.Serializer):
    count = serializers.IntegerField()
    Crm_Cd = serializers.IntegerField()

class Query5Serializer(serializers.Serializer):
    Areas = serializers.ListField(child=serializers.IntegerField())
    Crm_Cd = serializers.IntegerField()
    Weapon_Types = serializers.ListField(child=serializers.CharField())

class Query6Serializer(serializers.Serializer):
    upvote_count = serializers.IntegerField()
    DR_NO = serializers.IntegerField()
    
class Query7Serializer(serializers.Serializer):
    officer_name = serializers.CharField()
    total_upvotes = serializers.IntegerField()
    badge_number = serializers.CharField()

class Query8Serializer(serializers.Serializer):
    officer_name = serializers.CharField()
    total_areas = serializers.IntegerField()
    badge_number = serializers.CharField()
    
class Query9Serializer(serializers.Serializer):
    email = serializers.EmailField()
    badgeNumbers = serializers.ListField(child=serializers.CharField())
    DR_NO = serializers.IntegerField()

class AreaSerializer(serializers.Serializer):
    area_code = serializers.IntegerField()
    area_name = serializers.CharField()

class Query10Serializer(serializers.Serializer):
    voted_areas = serializers.ListField(child=AreaSerializer())
    name = serializers.CharField()