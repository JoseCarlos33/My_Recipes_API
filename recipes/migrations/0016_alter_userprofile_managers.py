# Generated by Django 4.0.2 on 2022-04-15 22:24

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_userprofile_groups_userprofile_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]