from extractor import extract_scores
from scorekeeping import update_scores


def handler(event, context):
    scores = extract_scores()
    update_scores(scores=scores)


if __name__ == "__main__":
    handler({}, "")
