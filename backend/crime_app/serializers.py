from rest_framework import serializers
from datetime import datetime
from crime_app.models import CrimeReport, OfficerUpvote, PoliceOfficer

class CrimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = '__all__'

class OfficerUpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerUpvote
        fields = '__all__'

class PoliceOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliceOfficer
        fields = '__all__'

class Query1Serializer(serializers.Serializer):
    count = serializers.IntegerField()
    Crm_Cd = serializers.IntegerField()

class Query5Serializer(serializers.Serializer):
    Areas = serializers.ListField(child=serializers.IntegerField())
    Crm_Cd = serializers.IntegerField()
    Weapon_Types = serializers.ListField(child=serializers.CharField())