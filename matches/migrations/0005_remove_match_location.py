# Generated by Django 4.0.10 on 2023-07-14 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0004_match_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='location',
        ),
    ]