from google.cloud import translate_v2 as translate


def translate_text(text, target="ko"):
    try:
        client = translate.Client()
        result = client.translate(text, target_language=target)
        return result["translatedText"]
    except Exception:
        return text
