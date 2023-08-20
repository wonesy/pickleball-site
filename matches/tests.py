# matches/forms.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Match
from .forms import MatchResultForm


class MatchModelTests(TestCase):
    def test_create_match(self):
        # Test creating a match object and assert that it's saved correctly
        User = get_user_model()
        user1 = User.objects.create_user(username="user1", password="testpassword")
        user2 = User.objects.create_user(username="user2", password="testpassword")

        match = Match.objects.create(
            week=1,
            player=user1,
            opponent=user2,
            deadline="2023-07-15",
            game1_score="21-19",
            game2_score="17-21",
            game3_score="21-18",
        )

        self.assertEqual(match.week, 1)
        self.assertEqual(match.player, user1)
        self.assertEqual(match.opponent, user2)
        # Add more assertions for other fields if needed

    def test_get_game_points_won(self):
        # Test the get_game_points_won() method
        match = Match.objects.create(
            week=1,
            player=get_user_model().objects.create_user(
                username="user1", password="testpassword"
            ),
            opponent=get_user_model().objects.create_user(
                username="user2", password="testpassword"
            ),
            deadline="2023-07-15",
            game1_score="21-18",
            game2_score="18-21",
            game3_score="21-19",
        )

        player_points, opponent_points = match.get_game_points_won()
        self.assertEqual(player_points, 60)  # 21 + 18 + 21
        self.assertEqual(opponent_points, 58)  # 18 + 21 + 19


class MatchViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_schedule_view(self):
        # Test the schedule view
        response = self.client.get(reverse("schedule", args=["testuser"]))
        self.assertEqual(response.status_code, 200)
        # Add more assertions for the template and context data if needed

    def test_submit_result_view(self):
        # Test the submit_result view with a form submission
        match = Match.objects.create(
            week=1,
            player=self.user,
            opponent=get_user_model().objects.create_user(
                username="testopponent", password="testpassword"
            ),
            deadline="2023-07-15",
            game1_score="21-19",
            game2_score="17-21",
            game3_score="21-18",
        )

        form_data = {
            "game1_score": "21-15",
            "game2_score": "21-18",
            "game3_score": "0-21",
        }
        response = self.client.post(
            reverse("submit_result", args=[match.id]), data=form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        # Add more assertions for the redirected page if needed


class MatchFormTests(TestCase):
    def test_match_result_form_valid_data(self):
        # Test the MatchResultForm with valid data
        form_data = {
            "game1_score": "21-19",
            "game2_score": "17-21",
            "game3_score": "21-18",
        }
        form = MatchResultForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_match_result_form_invalid_data(self):
        # Test the MatchResultForm with invalid data
        form_data = {
            "game1_score": "invalid-score",
            "game2_score": "17-21",
            "game3_score": "21-18",
        }
        form = MatchResultForm(data=form_data)
        self.assertFalse(form.is_valid())
