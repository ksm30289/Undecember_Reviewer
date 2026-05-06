import os
import json
from google.cloud import translate_v2 as translate


def translate_text(text, target="ko"):
    try:
        # 🔥 서비스 계정 강제 설정
        cred_path = "/tmp/gcp.json"

        if not os.path.exists(cred_path):
            with open(cred_path, "w") as f:
                f.write(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

        client = translate.Client()
        result = client.translate(text, target_language=target)
        return result["translatedText"]

    except Exception as e:
        print("번역 실패:", e)
        return text
