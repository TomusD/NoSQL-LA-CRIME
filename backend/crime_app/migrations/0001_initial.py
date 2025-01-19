# Generated by Django 3.1.12 on 2025-01-19 17:42

import crime_app.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrimeReport',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('DR_NO', models.IntegerField(unique=True)),
                ('Mocodes', models.TextField(blank=True, null=True)),
                ('date_info', djongo.models.fields.JSONField(blank=True, null=True)),
                ('area_info', djongo.models.fields.JSONField(blank=True, null=True)),
                ('crime_info', djongo.models.fields.JSONField(blank=True, null=True)),
                ('victim_info', djongo.models.fields.JSONField(blank=True, null=True)),
                ('premise_info', djongo.models.fields.JSONField(blank=True, null=True)),
                ('weapon_info', djongo.models.fields.JSONField(blank=True, null=True)),
                ('status_info', djongo.models.fields.JSONField(blank=True, null=True)),
                ('location_info', djongo.models.fields.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PoliceOfficer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('badge_number', models.CharField(max_length=5)),
                ('upvote_details', djongo.models.fields.ArrayField(blank=True, default=[], model_container=crime_app.models.OfficerUpvote)),
            ],
        ),
    ]
