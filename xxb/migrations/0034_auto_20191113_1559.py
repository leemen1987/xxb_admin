# Generated by Django 2.1.8 on 2019-11-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0033_auto_20191113_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadsite_info',
            name='SiteNo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
