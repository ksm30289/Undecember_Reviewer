from google_play_scraper import reviews, Sort
from datetime import datetime

from config import APP_ID, START_DATE
from translator import translate_text
from sheets import get_existing_review_ids


START_DT = datetime.strptime(START_DATE, "%Y-%m-%d")


def classify(score):
    if score <= 2:
        return "부정"
    elif score == 3:
        return "중립"
    return "긍정"


def fetch_reviews(lang, country, count=200):
    result, _ = reviews(
        APP_ID,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count
    )
    return result


def collect_reviews():
    review_sets = [
        {"lang": "ko", "country": "kr"},
        {"lang": "en", "country": "us"},
    ]

    rows_all = []
    rows_pos = []
    rows_neg = []
    rows_neu = []

    existing_ids = get_existing_review_ids("구글플레이 리뷰")

    seen = set()

    for setting in review_sets:
        lang = setting["lang"]
        country = setting["country"]

        print(f"리뷰 수집 중: lang={lang}, country={country}")

        result = fetch_reviews(lang, country)

        for r in result:
            review_id = r.get("reviewId", "")
            if review_id and review_id in seen:
                continue
            seen.add(review_id)

            created = r.get("at")
            if not created or created < START_DT:
                continue

            score = r.get("score", 0)
            content = str(r.get("content", "")).strip()
            user = str(r.get("userName", "")).strip()
            app_version = str(r.get("reviewCreatedVersion", "") or "").strip()

            if not content:
                continue

            category = classify(score)

            # 한국어는 원문 그대로, 영어는 한국어 번역
            if lang == "en":
                translated = translate_text(content, "ko")
            else:
                translated = content

            row = [
                datetime.now().strftime("%Y-%m-%d"),
                created.strftime("%Y-%m-%d"),
                lang,
                score,
                category,
                user,
                content,
                translated,
                review_id,
                app_version,
            ]

            rows_all.append(row)

            if category == "긍정":
                rows_pos.append(row)
            elif category == "부정":
                rows_neg.append(row)
            else:
                rows_neu.append(row)

    return rows_all, rows_pos, rows_neg, rows_neu
