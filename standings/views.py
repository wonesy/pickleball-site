# standings/views.py
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from matches.models import Match
from accounts.models import CustomUser


@login_required
def standings(request):
    players = CustomUser.objects.all()
    weeks = Match.objects.values_list("week", flat=True).distinct().order_by("week")

    standings_data = []

    for player in players:
        player_data = {
            "player": player.username,
            "points_by_week": [],
            "rating": player.rating,
        }

        for week in weeks:
            matches = Match.objects.filter(
                Q(player=player, week=week) | Q(opponent=player, week=week)
            )

            week_points = 0
            for match in matches:
                if match.player == player:
                    week_points += match.player_match_points or 0
                else:
                    week_points += match.opponent_match_points or 0

            player_data["points_by_week"].append(week_points)

        player_data["total_points"] = sum(player_data["points_by_week"])
        standings_data.append(player_data)

    standings_data = sorted(
        standings_data, key=lambda x: (x["total_points"], x["rating"]), reverse=True
    )

    rank = 1
    prev_total_points = None
    prev_rating = None

    # Assign ranks and save to the user model
    for player_data in standings_data:
        if (
            player_data["total_points"] != prev_total_points
            or player_data["rating"] != prev_rating
        ):
            player = CustomUser.objects.get(username=player_data["player"])
            player.rank = rank
            player.save()
            player_data["rank"] = rank  # Save rank in standings_data dictionary
            rank += 1
            prev_total_points = player_data["total_points"]
            prev_rating = player_data["rating"]
        else:
            # Same rank as previous player (tie)
            player = CustomUser.objects.get(username=player_data["player"])
            player.rank = rank - 1
            player.save()
            player_data["rank"] = rank - 1  # Save rank in standings_data dictionary

    return render(
        request, "standings.html", {"standings_data": standings_data, "weeks": weeks}
    )
