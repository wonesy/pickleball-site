# matches/models.py
from django.db import models
from django.conf import settings


class Match(models.Model):
    week = models.PositiveIntegerField()
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="home_matches"
    )
    opponent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="away_matches"
    )
    deadline = models.DateField()
    game1_score = models.CharField(max_length=5, blank=True, default="")
    game2_score = models.CharField(max_length=5, blank=True, default="")
    game3_score = models.CharField(max_length=5, blank=True, default="")

    # Need to include because looping over matches in schedule.html
    player_result = models.CharField(max_length=1, blank=True, default="")
    opponent_result = models.CharField(max_length=1, blank=True, default="")

    player_match_points = models.PositiveIntegerField(default=0)
    opponent_match_points = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update game points for player and opponent
        self.player.update_game_points()
        self.opponent.update_game_points()

        # Update match points for player and opponent
        self.player.update_match_points()
        self.opponent.update_match_points()

    def get_game_points_won(self):
        game_scores = [
            self.game1_score,
            self.game2_score,
            self.game3_score,
        ]
        player_points_won = 0
        opponent_points_won = 0

        for score in game_scores:
            if score:
                player_score, opponent_score = map(int, score.split("-"))
                player_points_won += player_score
                opponent_points_won += opponent_score

        return player_points_won, opponent_points_won

    def __str__(self):
        return f"Week {self.week}: {self.player.username} vs {self.opponent.username} by {self.deadline}"
