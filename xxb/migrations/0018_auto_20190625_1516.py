# Generated by Django 2.1.8 on 2019-06-25 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0017_auto_20190625_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gps_info',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
