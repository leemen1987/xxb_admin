# Generated by Django 2.1.8 on 2019-11-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0032_auto_20191113_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadid_to_busline',
            name='Rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]