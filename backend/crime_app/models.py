from django.db import models

class CrimeReport(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)
    DR_NO = models.IntegerField(unique=True)
    Date_Rptd = models.DateField()  
    DATE_OCC = models.DateField()
    TIME_OCC = models.TimeField()  

    AREA = models.IntegerField()
    AREA_NAME = models.CharField(max_length=100)
    Rpt_Dist_No = models.IntegerField()

    Crm_Cd = models.IntegerField()
    Crm_Cd_Desc = models.CharField(max_length=100)

    Mocodes = models.TextField()

    Vict_Age = models.IntegerField(null=True)
    Vict_Sex = models.CharField(max_length=5, null=True)
    Vict_Descent = models.CharField(max_length=5, null=True)

    Premis_Cd = models.IntegerField()
    Premis_Desc = models.CharField(max_length=100)

    Weapon_Used_Cd = models.IntegerField(default=0)
    Weapon_Desc = models.CharField(max_length=100, null=True, blank=True)

    Status = models.CharField(max_length=2)
    Status_Desc = models.CharField(max_length=15)

    Crm_Cd_1 = models.IntegerField()
    Crm_Cd_2 = models.IntegerField(null=True, blank=True)
    Crm_Cd_3 = models.IntegerField(null=True, blank=True)
    Crm_Cd_4 = models.IntegerField(null=True, blank=True)

    LOCATION = models.CharField(max_length=200)
    Cross_Street = models.CharField(max_length=200, null=True, blank=True)
    LAT = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    LON = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Crime Report {self.dr_no}"

class PoliceOfficer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    badge_number = models.CharField(max_length=50)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.badge_number})"