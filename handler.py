from score_extraction import extract_scores
from scorekeeping import update_game_score


def handler(event, context):
    # scores = extract_scores()

    # for score in scores:
    #     update_game_score(game_score=score)

    update_game_score(game_score={})


if __name__ == "__main__":
    handler({}, "")
