# scripts/generate_match_data.py

# Does not evenly distribute home/away matches
# Use count_user_matches to determine possible disparities
# If import error, run the following in home directory: export PYTHONPATH=$PYTHONPATH:/home

import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

# Configure Django settings
django.setup()

# Now you can import your models
from django.utils import timezone
from accounts.models import CustomUser  # Import the CustomUser model
from matches.models import Match  # Import the Match model
from datetime import timedelta  # Import timedelta to handle date changes


def delete_all_matches():
    # Delete all Match instances from the database
    Match.objects.all().delete()
    print("All match data has been deleted.")


def generate_and_save_round_robin_matches():
    players_list = list(CustomUser.objects.all())  # Fetch all users from the database
    if len(players_list) % 2 != 0:
        players_list.append(None)  # Add a dummy player to make the number even

    num_players = len(players_list)
    num_weeks = num_players - 1
    half_num_players = num_players // 2

    # Set the initial deadline date for the first week
    initial_deadline = timezone.now() + timedelta(
        days=7
    )  # Assuming one week from the current date

    for week in range(num_weeks):
        deadline = initial_deadline + timedelta(
            weeks=week
        )  # Increment the deadline for each week

        for i in range(half_num_players):
            if players_list[i] and players_list[num_players - 1 - i]:
                # Create the Match instance
                match = Match.objects.create(
                    week=week + 1,
                    player=players_list[i],
                    opponent=players_list[num_players - 1 - i],
                    deadline=deadline,  # Set the deadline for the current week
                )
                # Save the Match instance to the database
                match.save()

        players_list.insert(1, players_list.pop())  # Rotate players for the next round

    print("Match data has been generated and saved.")


if __name__ == "__main__":
    delete_all_matches()
    generate_and_save_round_robin_matches()
