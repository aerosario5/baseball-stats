import statsapi
import requests
import time
from datetime import datetime
from games.models import Game, Team
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

"""
Average length of games
Team records
Pitcher wins/losses/saves/innings pitched/# of pitches thrown
Team matchup records
Team at home vs away records
"""

def get_games_during_year(year=None, game_type=None):
    if not year:
        today = datetime.now()
        year = today.year
    start_date = str(year)+'-01-01'
    end_date = str(year)+'-12-31'
    games = statsapi.schedule(start_date=start_date, end_date=end_date, sportId=1)
    if game_type:
        games = [g for g in games if g['game_type'] == game_type]
    return games

def get_records(games):
    teams = {}
    for game in games:
        if game['status'] != 'Final':
            continue
        winning_team = game['winning_team']
        losing_team = game['losing_team']
        if winning_team not in teams:
            teams[winning_team] = {'wins': 0, 'losses': 0}
        if losing_team not in teams:
            teams[losing_team] = {'wins': 0, 'losses': 0}

        teams[winning_team]['wins'] += 1
        teams[losing_team]['losses'] += 1
    return teams

def get_box_attribute(game, attribute):
    box_score = statsapi.boxscore_data(game['game_id'])
    box_info = box_score['gameBoxInfo']
    for attr in box_info:
        if attr['label'] == attribute:
            return attr['value']
    return

def populate_games(games):
    for game in games:
        if game['status'] != 'Final':
            continue
        run_time = get_box_attribute(game, 'T')
        winning_team_id = ''
        losing_team_id = ''
        home_team_id = game['home_id']
        away_team_id = game['away_id']
        if game['winning_team'] == game['home_name']:
            winning_team_id = home_team_id
            losing_team_id = away_team_id
        elif game['winning_team'] == game['away_name']:
            winning_team_id = away_team_id
            losing_team_id = home_team_id
        try:
            game_entry = Game.objects.get(id=game['game_id'])
            print("Game {id} exists".format(id=game['game_id']))
        except ObjectDoesNotExist:
            print("Adding game {id}".format(id=game['game_id']))
            game_entry = Game(
                id=game['game_id'],
                home_team_id=home_team_id,
                home_team=game['home_team']
                away_team_id=away_team_id,
                away_team=game['away_team'],
                run_time=run_time,
                winning_team_id=winning_team_id,
                winning_team=game['winning_team'],
                losing_team=game['losing_team'],
                losing_team_id=losing_team_id,
                start_time=game['game_datetime'],
                game_type=game['game_type'],
                home_score=game['home_score'],
                away_score=game['away_score'],
            )
            game_entry.save()
