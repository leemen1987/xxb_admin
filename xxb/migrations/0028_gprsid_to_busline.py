# Generated by Django 2.1.8 on 2019-09-24 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0027_gps_info_backup'),
    ]

    operations = [
        migrations.CreateModel(
            name='gprsid_to_busline',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gprsid', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('busline', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('direction', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
        ),
    ]
