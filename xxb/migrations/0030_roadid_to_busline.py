# Generated by Django 2.1.8 on 2019-11-11 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0029_roadsite_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadID_to_BusLine',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('RoadID', models.CharField(blank=True, max_length=255, null=True)),
                ('BusLine', models.CharField(blank=True, max_length=255, null=True)),
                ('RoadType', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
