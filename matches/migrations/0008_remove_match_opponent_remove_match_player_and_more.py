# Generated by Django 4.0.10 on 2023-07-15 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0007_remove_match_away_player_remove_match_home_player_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='opponent',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player',
        ),
        migrations.AddField(
            model_name='match',
            name='away_player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='home_player',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='matches', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
