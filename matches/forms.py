# matches/forms.py
from django import forms

from .models import Match


class MatchResultForm(forms.ModelForm):
    game1_score = forms.CharField(max_length=5, label="Game 1 Score")
    game2_score = forms.CharField(max_length=5, label="Game 2 Score")
    game3_score = forms.CharField(max_length=5, label="Game 3 Score")

    class Meta:
        model = Match
        fields = ["game1_score", "game2_score", "game3_score"]

    def clean(self):
        cleaned_data = super().clean()
        game1_score = cleaned_data.get("game1_score")
        game2_score = cleaned_data.get("game2_score")
        game3_score = cleaned_data.get("game3_score")

        # Perform any additional validation if needed

        return cleaned_data
