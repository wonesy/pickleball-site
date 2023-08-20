from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from matches.models import Match


class StandingsViewTests(TestCase):
    def setUp(self):
        # Create some test users
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="testpassword"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="testpassword"
        )
        self.user3 = get_user_model().objects.create_user(
            username="user3", password="testpassword"
        )

    def create_match(
        self, week, player, opponent, player_match_points, opponent_match_points
    ):
        # Helper method to create a match
        return Match.objects.create(
            week=week,
            player=player,
            opponent=opponent,
            deadline="2023-07-15",
            player_match_points=player_match_points,
            opponent_match_points=opponent_match_points,
        )

    def test_standings_view(self):
        # Log in the user
        self.client.login(username="user1", password="testpassword")

        # Test the standings view
        match1 = self.create_match(1, self.user1, self.user2, 10, 40)
        match2 = self.create_match(1, self.user1, self.user3, 40, 0)
        match3 = self.create_match(2, self.user2, self.user3, 40, 20)

        response = self.client.get(reverse("standings"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "standings.html")

        # Add more assertions to check the context data and rendering of the template
        # For example:
        self.assertIn("standings_data", response.context)
        self.assertIn("weeks", response.context)
        standings_data = response.context["standings_data"]
        self.assertEqual(
            len(standings_data), 3
        )  # Check the number of players in standings

        # Assuming you have sorted standings_data in the view, you can check the expected order
        self.assertEqual(standings_data[0]["player"], "user2")
        self.assertEqual(standings_data[0]["rank"], 1)
        self.assertEqual(standings_data[0]["total_points"], 80)  # 40 + 40

        self.assertEqual(standings_data[1]["player"], "user1")
        self.assertEqual(standings_data[1]["rank"], 2)
        self.assertEqual(standings_data[1]["total_points"], 50)  # 10 + 40

        self.assertEqual(standings_data[2]["player"], "user3")
        self.assertEqual(standings_data[2]["rank"], 3)
        self.assertEqual(standings_data[2]["total_points"], 20)  # 0 + 20

        # Add more assertions to check the points, ratings, and other data in standings_data
