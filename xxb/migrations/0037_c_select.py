# Generated by Django 2.1.8 on 2019-12-03 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0036_roadid_to_busline_new'),
    ]

    operations = [
        migrations.CreateModel(
            name='c_select',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('select', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('Rank', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
