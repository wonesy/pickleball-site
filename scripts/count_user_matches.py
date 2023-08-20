# scripts/count_user_matches.py

# Count user home and away matches
# Manually adjust in admin interface
# If import error, run the following in home directory: export PYTHONPATH=$PYTHONPATH:/home

import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

# Configure Django settings
django.setup()

# Now you can import your models
from accounts.models import CustomUser
from matches.models import Match


def count_matches_for_all_users():
    users = CustomUser.objects.all()

    for user in users:
        # Count matches where the user is a player
        num_player_matches = Match.objects.filter(player=user).count()

        # Count matches where the user is an opponent
        num_opponent_matches = Match.objects.filter(opponent=user).count()

        print(f"User: {user.username}")
        print(
            f"Number of matches where {user.username} is a player: {num_player_matches}"
        )
        print(
            f"Number of matches where {user.username} is an opponent: {num_opponent_matches}"
        )
        print()


if __name__ == "__main__":
    count_matches_for_all_users()
