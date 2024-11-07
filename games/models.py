from django.db import models

# Create your models here.


class Game(models.Model):
    home_team_id = models.CharField(max_length=500)
    home_team = models.CharField(max_length=500, default='')
    away_team_id = models.CharField(max_length=500)
    away_team = models.CharField(max_length=500, default='')
    run_time = models.CharField(max_length=500)
    winning_team_id = models.CharField(max_length=500)
    winning_team = models.CharField(max_length=500, default='')
    losing_team_id = models.CharField(max_length=500)
    losing_team = models.CharField(max_length=500, default='')
    start_time = models.DateTimeField(max_length=500)
    game_type = models.CharField(max_length=10)
    home_score = models.IntegerField()
    away_score = models.IntegerField()

class Team(models.Model):
    team_name = models.CharField(max_length=500)
