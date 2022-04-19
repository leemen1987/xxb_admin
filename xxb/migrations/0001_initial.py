# Generated by Django 2.1.7 on 2019-03-13 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APItest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sysid', models.CharField(blank=True, max_length=255, null=True)),
                ('reqid', models.CharField(blank=True, max_length=255, null=True)),
                ('protover', models.CharField(blank=True, max_length=255, null=True)),
                ('servicecode', models.CharField(blank=True, max_length=255, null=True)),
                ('requesttime', models.CharField(blank=True, max_length=255, null=True)),
                ('signdata', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='busline',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('station_id', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('GprsId', models.CharField(blank=True, max_length=255)),
                ('OrderNo', models.CharField(blank=True, max_length=255)),
                ('direction', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('even_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.CharField(blank=True, max_length=255, null=True)),
                ('start_time', models.CharField(blank=True, max_length=255, null=True)),
                ('end_time', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
