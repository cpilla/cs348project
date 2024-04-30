from django import forms
from .models import Player, Team

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = "__all__"

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "wins", "losses")