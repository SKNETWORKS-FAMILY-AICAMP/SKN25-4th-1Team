from __future__ import annotations

import os

import requests
from dotenv import load_dotenv

from frontend.webui.data_loader import BASE_DIR


load_dotenv(BASE_DIR / ".env")

DEFAULT_FASTAPI_URL = "http://127.0.0.1:8000/api/chat"
FASTAPI_URL = os.getenv("FASTAPI_URL", DEFAULT_FASTAPI_URL)


def get_chat_response(question: str, selected_device: str, thread_id: str) -> str:
    payload = {
        "question": question,
        "selected_device": selected_device,
        "thread_id": thread_id,
    }

    try:
        response = requests.post(FASTAPI_URL, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException:
        return (
            "FastAPI 서버와 아직 연결되지 않았습니다. 백엔드가 먼저 올라오는 동안 잠시 후 다시 시도해주세요."
        )
    except ValueError:
        return "백엔드 응답을 해석하지 못했습니다. 서버 로그를 확인해주세요."

    answer = result.get("answer") if isinstance(result, dict) else None
    if isinstance(answer, str) and answer.strip():
        return answer.strip()

    return "답변을 생성하지 못했습니다. 잠시 후 다시 시도해주세요."
