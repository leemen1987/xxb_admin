# Generated by Django 2.1.8 on 2019-11-21 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0034_auto_20191113_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadid_to_busline',
            name='Line_info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
