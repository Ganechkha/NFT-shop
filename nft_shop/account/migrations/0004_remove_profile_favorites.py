# Generated by Django 5.1.1 on 2024-10-09 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favorites',
        ),
    ]
