# Generated by Django 2.1.8 on 2019-11-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0030_roadid_to_busline'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadid_to_busline',
            name='Rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
