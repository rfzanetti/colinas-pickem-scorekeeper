import requests

from teams import TEAMS_MAPPING

COLINAS_PICKEM_API_BASE_URL = "https://colinas-pickem-api.herokuapp.com"

GAME_NOT_STARTED_STATUS = "NOT_STARTED"
GAME_LIVE_STATUS = "LIVE"
GAME_FINAL_STATUS = "FINAL"

PICK_SCORE_PER_CORRECT_GUESSES = {
    1: 12,
    2: 10,
    3: 8,
    0: 0
}


def update_game_score(game_score):
    print(f"Updating game {game_score}")

    game_params = {
        "home_team": TEAMS_MAPPING[game_score["home"]],
        "away_team": TEAMS_MAPPING[game_score["away"]]
    }

    game = requests.get(
        url=f"{COLINAS_PICKEM_API_BASE_URL}/schedule", params=game_params).json()

    if not game:
        return

    update_game_score_and_status(game=game[0], game_score=game_score)
    update_pick_scores(game=game[0], game_score=game_score)


def update_game_score_and_status(game, game_score):
    game_id = game["id"]

    print(f"Updating game with ID {game_id}")

    score_body = {
        "home_team_score": game_score["home_score"],
        "away_team_score": game_score["away_score"],
        "status": game_score["status"]
    }

    requests.patch(
        url=f"{COLINAS_PICKEM_API_BASE_URL}/game/{game_id}", json=score_body)


def update_pick_scores(game, game_score):

    if game["status"] == GAME_FINAL_STATUS or game_score["status"] != GAME_FINAL_STATUS:
        print(f"Game status did not changed to FINAL. Ignoring... {game}")
        return

    print(f"Updating scores for game {game['id']}")

    picks = get_game_picks(game=game)
    winner = get_game_winner(game=game)
    correct_pick_score = get_correct_pick_score(picks=picks, winner=winner)

    for pick in picks:
        if pick["picked_team"] == winner:
            update_pick_score(pick=pick, score=correct_pick_score)
        else:
            update_pick_score(pick=pick, score=0)


def update_pick_score(pick, score):
    pick_url = f"{COLINAS_PICKEM_API_BASE_URL}/pick/user/{pick['user_id']}/game/{pick['game_id']}"

    pick_payload = {"score": score}

    requests.patch(url=pick_url, json=pick_payload)


def get_game_picks(game):
    picks_params = {
        "game_id": game["id"]
    }

    return requests.get(url=f"{COLINAS_PICKEM_API_BASE_URL}/pick", params=picks_params).json()


def get_game_winner(game):
    if game["home_team_score"] > game["away_team_score"]:
        return "H"
    elif game["away_team_score"] > game["home_team_score"]:
        return "A"
    else:
        return "T"


def get_correct_pick_score(picks, winner):
    correct_pick_count = len(
        [pick for pick in picks if pick["picked_team"] == winner])
    return PICK_SCORE_PER_CORRECT_GUESSES[correct_pick_count]
