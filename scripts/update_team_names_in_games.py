from games.models import Game, Team

team_objects = Team.objects.all()
teams = {str(team.id): team.team_name for team in team_objects}

def update_team_names_in_games(games = []):
    print(teams)
    if not games:
        games = Game.objects.all()
    for game in games:
        game.home_team = teams[game.home_team_id]
        game.away_team = teams[game.away_team_id]
        game.losing_team = teams[game.losing_team_id]
        game.winning_team = teams[game.winning_team_id]
        game.save()
