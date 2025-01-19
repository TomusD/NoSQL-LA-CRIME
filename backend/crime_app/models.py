from djongo import models
from django.utils import timezone

# Crime report model
class CrimeReport(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    DR_NO = models.IntegerField(unique=True)
    Mocodes = models.TextField(null=True, blank=True)

    date_info = models.JSONField(null=True, blank=True)
    area_info = models.JSONField(null=True, blank=True)
    crime_info = models.JSONField(null=True, blank=True)
    victim_info = models.JSONField(null=True, blank=True)
    premise_info = models.JSONField(null=True, blank=True)
    weapon_info = models.JSONField(null=True, blank=True)
    status_info = models.JSONField(null=True, blank=True)
    location_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Crime Report {self.DR_NO}"
    
# Upvote details for each officer
class OfficerUpvote(models.Model):
    crime_report_id = models.CharField(max_length=24)
    DR_NO = models.IntegerField()
    Date_Time_OCC = models.DateTimeField()
    Crm_Cd = models.IntegerField()   
    AREA = models.IntegerField()
    AREA_NAME = models.CharField(max_length=100)   
    Weapon_Used_Cd = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

# Police officer model
class PoliceOfficer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    badge_number = models.CharField(max_length=5)

    upvote_details = models.ArrayField(
        model_container=OfficerUpvote,
        default=[],
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.badge_number})"