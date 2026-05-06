import os
import re
import html
from google.cloud import translate_v2 as translate

from config import GOOGLE_SERVICE_ACCOUNT_JSON, GLOSSARY_SHEET
from sheets import get_records


_glossary_cache = None


def setup_google_credentials():
    cred_path = "/tmp/gcp.json"

    if not os.path.exists(cred_path):
        with open(cred_path, "w", encoding="utf-8") as f:
            f.write(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path


def load_glossary():
    global _glossary_cache

    if _glossary_cache is not None:
        return _glossary_cache

    try:
        records = get_records(GLOSSARY_SHEET)
    except Exception as e:
        print("용어집 로드 실패:", e)
        _glossary_cache = []
        return _glossary_cache

    glossary = []

    for row in records:
        source = str(row.get("원문", "")).strip()
        target = str(row.get("번역", "")).strip()

        if not source or not target:
            continue

        glossary.append({
            "source": source,
            "target": target,
        })

    # 긴 용어 우선 치환
    glossary.sort(key=lambda x: len(x["source"]), reverse=True)

    _glossary_cache = glossary
    print(f"용어집 로드 완료: {len(glossary)}개")

    return _glossary_cache


def protect_terms(text, glossary):
    protected = text
    mapping = {}

    for i, item in enumerate(glossary):
        source = item["source"]
        target = item["target"]
        token = f"__TERM_{i}__"

        pattern = re.compile(re.escape(source), re.IGNORECASE)

        if pattern.search(protected):
            protected = pattern.sub(token, protected)
            mapping[token] = target

    return protected, mapping


def restore_terms(text, mapping):
    restored = text

    for token, target in mapping.items():
        restored = restored.replace(token, target)

    return restored


def translate_text(text, target="ko"):
    if not text:
        return ""

    try:
        setup_google_credentials()

        glossary = load_glossary()

        protected_text, mapping = protect_terms(text, glossary)

        client = translate.Client()

        result = client.translate(
            protected_text,
            target_language=target,
            format_="text",
        )

        translated = result.get("translatedText", "")
        translated = html.unescape(translated)

        translated = restore_terms(translated, mapping)

        return translated

    except Exception as e:
        print("번역 실패:", e)
        return text
