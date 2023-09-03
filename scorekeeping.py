import requests

from teams import TEAMS_MAPPING

COLINAS_PICKEM_API_BASE_URL = "https://colinas.vercel.app/api"


def update_scores(scores):
    payload = make_payload(scores)

    for game in payload["games"]:
        print(f"UPDATING [{game}]")

    url = f"{COLINAS_PICKEM_API_BASE_URL}/games"
    response = requests.patch(url=url, json=payload)

    print(f"Response {response.status_code}: {response.text}")


def make_payload(scores):
    return {"games": [format_score(score) for score in scores]}


def format_score(game_score):
    return {
        "homeScore": game_score["home_score"],
        "awayScore": game_score["away_score"],
        "homeTeam": TEAMS_MAPPING[game_score["home"]],
        "awayTeam": TEAMS_MAPPING[game_score["away"]],
        "status": game_score["status"]
    }
