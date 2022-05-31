from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Games(models.Model):
    player = models.ManyToManyField(User)
    date = models.DateField()
    winner = models.CharField(max_length=25)

#to string prints out the name of the players
    def __str__(self):
        players = self.player.all()
        string = ''
        for player in players:
            string = string + 'player: ' + str(player.username) + ' '
        return string
