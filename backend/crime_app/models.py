from djongo import models
from django.utils import timezone

# FIX NULLS AND FIELDS

class DateObject(models.Model):
    Date_Rptd = models.DateField(null=True, blank=True)
    DATE_OCC = models.DateField(null=True, blank=True)
    TIME_OCC = models.IntegerField(null=True, blank=True)
    Date_Time_OCC = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class AreaObject(models.Model):
    AREA = models.IntegerField()
    AREA_NAME = models.CharField(max_length=100, null=True, blank=True)
    Rpt_Dist_No = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class CrimeObject(models.Model):
    Crm_Cd = models.IntegerField()
    Crm_Cd_Desc = models.CharField(max_length=100, null=True, blank=True)
    Crime_Codes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True


class VictimObject(models.Model):
    Vict_Age = models.IntegerField(null=True, blank=True)
    Vict_Sex = models.CharField(max_length=5, null=True, blank=True)
    Vict_Descent = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        abstract = True


class PremiseObject(models.Model):
    Premis_Cd = models.FloatField(null=True, blank=True)
    Premis_Desc = models.CharField(max_length=100,null=True, blank=True)

    class Meta:
        abstract = True


class WeaponObject(models.Model):
    Weapon_Used_Cd = models.IntegerField(default=0, null=True, blank=True)
    Weapon_Desc = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class StatusObject(models.Model):
    Status = models.CharField(max_length=2,null=True, blank=True)
    Status_Desc = models.CharField(max_length=15,null=True, blank=True)

    class Meta:
        abstract = True


class LocationObject(models.Model):
    LOCATION = models.CharField(max_length=200,null=True, blank=True)
    Cross_Street = models.CharField(max_length=200, null=True, blank=True)
    LAT = models.FloatField(null=True, blank=True)
    LON = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True


class CrimeReport(models.Model):
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Crime Report {self.DR_NO}"

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


class PoliceOfficer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    badge_number = models.CharField(max_length=50)

    upvote_details = models.ArrayField(
        model_container=OfficerUpvote,
        default=[],
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.badge_number})"