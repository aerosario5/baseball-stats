from baseball_stats.games.models import Game

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
