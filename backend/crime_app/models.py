from djongo import models
from django.utils import timezone

class DateObject(models.Model):
    Date_Rptd = models.DateField()
    DATE_OCC = models.DateField()
    TIME_OCC = models.TimeField()
    Date_Time_OCC = models.DateTimeField()

    class Meta:
        abstract = True


class AreaObject(models.Model):
    AREA = models.IntegerField()
    AREA_NAME = models.CharField(max_length=100)
    Rpt_Dist_No = models.IntegerField()

    class Meta:
        abstract = True


class CrimeObject(models.Model):
    Crm_Cd = models.IntegerField()
    Crm_Cd_Desc = models.CharField(max_length=100)
    Crime_Codes = models.JSONField()

    class Meta:
        abstract = True


class VictimObject(models.Model):
    Vict_Age = models.IntegerField(null=True)
    Vict_Sex = models.CharField(max_length=5, null=True)
    Vict_Descent = models.CharField(max_length=5, null=True)

    class Meta:
        abstract = True


class PremiseObject(models.Model):
    Premis_Cd = models.FloatField()
    Premis_Desc = models.CharField(max_length=100)

    class Meta:
        abstract = True


class WeaponObject(models.Model):
    Weapon_Used_Cd = models.IntegerField(default=0)
    Weapon_Desc = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class StatusObject(models.Model):
    Status = models.CharField(max_length=2)
    Status_Desc = models.CharField(max_length=15)

    class Meta:
        abstract = True


class LocationObject(models.Model):
    LOCATION = models.CharField(max_length=200)
    Cross_Street = models.CharField(max_length=200, null=True, blank=True)
    LAT = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    LON = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    class Meta:
        abstract = True


class CrimeReport(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)
    DR_NO = models.IntegerField(unique=True)
    Mocodes = models.TextField()


    date_object = models.EmbeddedField(model_container=DateObject)
    area_object = models.EmbeddedField(model_container=AreaObject)
    crime_object = models.EmbeddedField(model_container=CrimeObject)
    victim_object = models.EmbeddedField(model_container=VictimObject)
    premise_object = models.EmbeddedField(model_container=PremiseObject)
    weapon_object = models.EmbeddedField(model_container=WeaponObject)
    status_object = models.EmbeddedField(model_container=StatusObject)
    location_object = models.EmbeddedField(model_container=LocationObject)

    def __str__(self):
        return f"Crime Report {self.DR_NO}"

class OfficerUpvote(models.Model):
    crime_report_id = models.CharField(max_length=24)
    DR_NO = models.IntegerField()
    
    date_occ = models.DateField()
    time_occ = models.TimeField()  # optional
    crm_cd = models.IntegerField()
    
    area = models.IntegerField()
    area_name = models.CharField(max_length=100)
    
    weapon_used_cd = models.IntegerField()
    
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