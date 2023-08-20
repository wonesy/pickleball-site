# matches/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.models import CustomUser
from .models import Match
from .forms import MatchResultForm


@login_required
def schedule(request, username):
    requested_user = CustomUser.objects.get(username=username)
    matches = Match.objects.filter(
        Q(player=requested_user) | Q(opponent=requested_user)
    ).order_by("week")
    return render(
        request, "schedule.html", {"matches": matches, "requested_user": requested_user}
    )


def handle_forfeit(match, forfeit):
    if forfeit == "player":
        match.player_result = "L"
        match.opponent_result = "W"
        match.player_match_points = 0
        match.opponent_match_points = 40
    elif forfeit == "opponent":
        match.player_result = "W"
        match.opponent_result = "L"
        match.player_match_points = 40
        match.opponent_match_points = 0
    match.game1_score = "0-0"
    match.game2_score = "0-0"
    match.game3_score = "0-0"
    match.save()


def handle_submission(request, match):
    form = MatchResultForm(request.POST)

    if form.is_valid():
        game1_score = form.cleaned_data["game1_score"]
        game2_score = form.cleaned_data["game2_score"]
        game3_score = form.cleaned_data["game3_score"]

        # Determine the winner based on the game scores
        player_wins = 0
        opponent_wins = 0

        game1_player_score, game1_opponent_score = map(int, game1_score.split("-"))
        game2_player_score, game2_opponent_score = map(int, game2_score.split("-"))
        game3_player_score, game3_opponent_score = map(int, game3_score.split("-"))

        if game1_player_score > game1_opponent_score:
            player_wins += 1
        elif game1_player_score < game1_opponent_score:
            opponent_wins += 1

        if game2_player_score > game2_opponent_score:
            player_wins += 1
        elif game2_player_score < game2_opponent_score:
            opponent_wins += 1

        if game3_player_score > game3_opponent_score:
            player_wins += 1
        elif game3_player_score < game3_opponent_score:
            opponent_wins += 1

        # Determine the overall winner
        games_won_match_points = {0: 10, 1: 20, 2: 40, 3: 40}
        if player_wins > opponent_wins:
            match.player_result = "W"
            match.opponent_result = "L"
        elif opponent_wins > player_wins:
            match.player_result = "L"
            match.opponent_result = "W"
        match.player_match_points = games_won_match_points[player_wins]
        match.opponent_match_points = games_won_match_points[opponent_wins]

        match.game1_score = game1_score
        match.game2_score = game2_score
        match.game3_score = game3_score
        match.save()


def submit_result(request, match_id):
    match = Match.objects.get(pk=match_id)

    if request.method == "POST":
        forfeit = request.POST.get("forfeit")

        if forfeit in ["player", "opponent"]:
            handle_forfeit(match, forfeit)
        else:
            handle_submission(request, match)

        return redirect("schedule", username=request.user)

    form = MatchResultForm()
    return render(request, "submit_result.html", {"match": match, "form": form})
