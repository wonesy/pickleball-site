# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\d{3}-\d{3}-\d{4}$",
        message="Phone number must be entered in the format: '112-358-1321'.",
    )
    phone = models.CharField(
        max_length=12, null=True, blank=True, validators=[phone_regex]
    )
    game_points_won = models.PositiveIntegerField(default=0)
    game_points_lost = models.PositiveIntegerField(default=0)
    match_points_won = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    def update_game_points(self):
        home_matches = self.home_matches.all()
        away_matches = self.away_matches.all()

        game_points_won = sum(
            match.get_game_points_won()[0] for match in home_matches
        ) + sum(match.get_game_points_won()[1] for match in away_matches)
        game_points_lost = sum(
            match.get_game_points_won()[1] for match in home_matches
        ) + sum(match.get_game_points_won()[0] for match in away_matches)

        self.game_points_won = game_points_won
        self.game_points_lost = game_points_lost
        self.save()

    def update_match_points(self):
        home_matches = self.home_matches.all()
        away_matches = self.away_matches.all()

        match_points_won = sum(
            match.player_match_points for match in home_matches
        ) + sum(match.opponent_match_points for match in away_matches)

        self.match_points_won = match_points_won
        self.save()

    @property
    def rating(self):
        total_game_points = self.game_points_won + self.game_points_lost
        if total_game_points == 0:
            return "0.000"
        rating_value = self.game_points_won / total_game_points
        return "{:.3f}".format(rating_value)
