from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class LobbyGames(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    second_player = models.CharField(max_length=25, null=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.owner)
