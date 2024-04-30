from django.db import models
from django.forms import ModelChoiceField, Form
# Create your models here.
class Player(models.Model):
    puid = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length=50)
    purdue_email = models.CharField(max_length=50)
    POSITIONS = (("H", "Hitter"), ("S", "Setter"), ("L", "Libero"), ("F", "Flex"))
    position = models.CharField(max_length=1, choices=POSITIONS)

class Team(models.Model):
    name = models.CharField(max_length=100)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    players = models.ManyToManyField(Player, through='PlayerTeam')

class PlayerTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)



