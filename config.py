import os
import json


def required(name):
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"환경변수 누락: {name}")
    return v


SPREADSHEET_ID = required("SPREADSHEET_ID")
GOOGLE_SERVICE_ACCOUNT_JSON = json.loads(required("GOOGLE_SERVICE_ACCOUNT_JSON"))

APP_ID = required("GOOGLE_PLAY_APP_ID")

START_DATE = os.getenv("GP_REVIEW_START_DATE", "2026-01-01")

# 번역
USE_TRANSLATE = True
