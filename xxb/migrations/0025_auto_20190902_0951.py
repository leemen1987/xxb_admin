# Generated by Django 2.1.8 on 2019-09-02 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0024_edit_log_openid'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal_offer',
            name='breakfast_check',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='meal_offer',
            name='dinner_check',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='meal_offer',
            name='lunch_check',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]