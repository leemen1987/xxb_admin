# Generated by Django 2.1.8 on 2019-05-07 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xxb', '0007_meal_offer_user_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_info',
            old_name='opendi',
            new_name='openid',
        ),
    ]
