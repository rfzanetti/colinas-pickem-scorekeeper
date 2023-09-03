import requests

from bs4 import BeautifulSoup

SCOREBOARD_URL = "https://www.cbssports.com/nfl/scoreboard/"

GAME_NOT_STARTED_STATUS = "not_started"
GAME_LIVE_STATUS = "live"
GAME_FINAL_STATUS = "final"


def extract_scores():
    page = requests.get(SCOREBOARD_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    game_cards = soup.find_all(class_="single-score-card")
    games = [parse_game(game) for game in game_cards]

    return [game for game in games if game]


def parse_game(game):

    score = game_score(game)
    status = game_status(game)

    if score and status:
        return {
            **score,
            **status
        }


def game_score(game):
    obj = dict()

    teams = game.find_all(class_="team-name-link")
    scores = game.find_all(class_="total")

    if teams:
        obj["away"] = teams[0].get_text()
        obj["home"] = teams[1].get_text()

        if scores:
            obj["away_score"] = scores[1].get_text()
            obj["home_score"] = scores[2].get_text()
        else:
            obj["away_score"] = 0
            obj["home_score"] = 0

    return obj


def game_status(game):
    status = game.find(class_="game-status")

    if not status:
        return

    if "pregame" in status["class"]:
        return {"status": GAME_NOT_STARTED_STATUS}
    elif "postgame" in status["class"]:
        return {"status": GAME_FINAL_STATUS}
    else:
        return {"status": GAME_LIVE_STATUS}


if __name__ == "__main__":
    games = extract_scores()
    for game in games:
        print(game)
