import os
import uuid

import requests


def generate_thread_id():
    return str(uuid.uuid4())


def chat_with_fastapi(question, selected_device, thread_id):
    fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000/api/chat")
    payload = {
        "question": question,
        "selected_device": selected_device or "선택하지 않음",
        "thread_id": thread_id,
    }

    try:
        response = requests.post(fastapi_url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("answer") or "답변을 생성하지 못했습니다. 잠시 후 다시 시도해주세요."
    except requests.RequestException:
        return "현재 챗봇 서버와 연결되지 않았습니다. FastAPI 서버 상태를 확인한 뒤 다시 시도해주세요."


def fetch_nearest_centers(latitude, longitude):
    api_key = os.getenv("KAKAO_API_KEY")
    if not api_key:
        return []

    try:
        response = requests.get(
            "https://dapi.kakao.com/v2/local/search/keyword.json",
            headers={"Authorization": f"KakaoAK {api_key}"},
            params={
                "query": "삼성전자 서비스센터",
                "x": longitude,
                "y": latitude,
                "radius": 5000,
                "sort": "distance",
            },
            timeout=10,
        )
        response.raise_for_status()
        documents = response.json().get("documents", [])[:3]
    except requests.RequestException:
        return []

    centers = []
    for item in documents:
        distance = int(item.get("distance") or 0)
        centers.append(
            {
                "name": item.get("place_name", "서비스센터"),
                "address": item.get("road_address_name") or item.get("address_name", ""),
                "distance_m": distance,
                "distance_label": f"{distance}m" if distance < 1000 else f"{distance / 1000:.1f}km",
                "phone": item.get("phone", ""),
                "lat": item.get("y"),
                "lng": item.get("x"),
                "place_url": item.get("place_url", ""),
            }
        )
    return centers
