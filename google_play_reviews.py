from google_play_scraper import reviews, Sort
from datetime import datetime

from config import APP_ID, START_DATE
from translator import translate_text


START_DT = datetime.strptime(START_DATE, "%Y-%m-%d")


def classify(score):
    if score <= 2:
        return "부정"
    elif score == 3:
        return "중립"
    return "긍정"


def collect_reviews():
    result, _ = reviews(
        APP_ID,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=200
    )

    rows_all = []
    rows_pos = []
    rows_neg = []
    rows_neu = []

    for r in result:
        created = r["at"]

        if created < START_DT:
            continue

        score = r["score"]
        content = r["content"]
        user = r["userName"]

        lang = "en"

        # 번역
        translated = translate_text(content, "ko")

        category = classify(score)

        row = [
            datetime.now().strftime("%Y-%m-%d"),
            created.strftime("%Y-%m-%d"),
            lang,
            score,
            category,
            user,
            content,
            translated,
        ]

        rows_all.append(row)

        if category == "긍정":
            rows_pos.append(row)
        elif category == "부정":
            rows_neg.append(row)
        else:
            rows_neu.append(row)

    return rows_all, rows_pos, rows_neg, rows_neu
