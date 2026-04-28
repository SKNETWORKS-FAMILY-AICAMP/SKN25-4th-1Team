import json
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "processed"
FAQ_PATH = DATA_DIR / "faq" / "faq_data_v4.csv"
DEVICE_PATH = DATA_DIR / "self-repair-list.json"

FAQ_CATEGORIES = [
    "전원/배터리/충전",
    "블루투스",
    "멈춤/오류/꺼짐",
    "설정",
    "데이터",
    "네트워크/WI-FI",
    "카메라/갤러리",
    "디스플레이",
    "애플리케이션",
    "전화/문자",
    "센서/연결",
    "소리/진동",
    "업데이트",
    "사양/구성품",
    "액세서리",
    "이동통신서비스",
    "기타/주의사항",
]

FAQ_TOPICS = ["배터리", "충전", "네트워크", "디스플레이", "카메라", "업데이트"]

POPULAR_FALLBACK_QUESTIONS = [
    "배터리가 빨리 닳아요",
    "충전이 되지 않아요",
    "와이파이가 자주 끊겨요",
    "화면이 멈추고 꺼져요",
    "카메라 초점이 맞지 않아요",
    "서비스센터를 찾고 싶어요",
]

FAQ_FALLBACK_ITEMS = [
    {
        "title": "배터리가 빨리 닳을 때 확인해야 할 항목은 무엇인가요?",
        "topic": "배터리",
        "tag": "배터리",
        "content": (
            "배터리 사용 시간이 급격히 줄어든 경우 화면 밝기, 백그라운드 앱, "
            "고주사율 설정, 위치 서비스, 네트워크 사용량을 먼저 확인해 주세요. "
            "배터리 보호 설정과 절전 모드를 적용한 뒤에도 개선되지 않으면 진단 또는 서비스센터 점검이 필요할 수 있습니다."
        ),
    },
    {
        "title": "충전이 되지 않을 때 가장 먼저 확인할 것은 무엇인가요?",
        "topic": "충전",
        "tag": "충전",
        "content": "충전기, 케이블, 충전 단자 오염 여부와 무선/유선 충전 상태를 순서대로 확인해 주세요.",
    },
    {
        "title": "와이파이가 자주 끊길 때 해결 방법이 있나요?",
        "topic": "네트워크",
        "tag": "와이파이",
        "content": "공유기 재부팅, 저장된 네트워크 삭제 후 재연결, 네트워크 설정 초기화를 차례로 시도해볼 수 있습니다.",
    },
    {
        "title": "화면이 멈추거나 터치가 잘 안 될 때는 어떻게 해야 하나요?",
        "topic": "디스플레이",
        "tag": "화면",
        "content": "강제 재시작, 안전 모드 점검, 보호필름 상태 확인 후에도 지속되면 하드웨어 점검이 필요할 수 있습니다.",
    },
    {
        "title": "카메라 초점이 잘 맞지 않을 때 점검할 부분은 무엇인가요?",
        "topic": "카메라",
        "tag": "카메라",
        "content": "렌즈 오염 여부를 닦아낸 뒤 카메라 앱 설정 초기화와 다른 촬영 모드 테스트를 진행해 주세요.",
    },
]


def topic_to_icon_key(topic):
    text = str(topic or "").strip().lower()

    if any(keyword in text for keyword in ["배터리", "battery"]):
        return "battery"
    if any(keyword in text for keyword in ["충전", "charge", "charging"]):
        return "charging"
    if any(keyword in text for keyword in ["와이파이", "wifi", "wi-fi", "네트워크", "network"]):
        return "wifi"
    if any(keyword in text for keyword in ["화면", "디스플레이", "display", "screen"]):
        return "display"
    if any(keyword in text for keyword in ["카메라", "camera"]):
        return "camera"
    if any(keyword in text for keyword in ["업데이트", "update", "software"]):
        return "update"
    return "faq"


def load_device_data():
    if not DEVICE_PATH.exists():
        return {}

    with DEVICE_PATH.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def load_faq_data():
    if not FAQ_PATH.exists():
        return pd.DataFrame(
            columns=[
                "title",
                "symptom_category",
                "url",
                "viewCnt",
                "exposureDate",
                "cleaned_content",
            ]
        )

    df = pd.read_csv(FAQ_PATH)
    required_defaults = {
        "symptom_category": "기타/주의사항",
        "title": "",
        "url": "",
        "cleaned_content": "",
        "viewCnt": 0,
        "exposureDate": None,
    }
    for col, default in required_defaults.items():
        if col not in df.columns:
            df[col] = default

    df["symptom_category"] = df["symptom_category"].fillna("기타/주의사항").astype(str)
    df["title"] = df["title"].fillna("").astype(str)
    df["url"] = df["url"].fillna("").astype(str)
    df["cleaned_content"] = df["cleaned_content"].fillna("").astype(str)
    df["viewCnt"] = pd.to_numeric(df["viewCnt"], errors="coerce").fillna(0).astype(int)
    df["exposureDate"] = pd.to_datetime(df["exposureDate"], errors="coerce")
    return df


def load_popular_question_items(limit=6):
    faq_df = load_faq_data()
    if faq_df.empty:
        return [
            {**item, "topic_key": topic_to_icon_key(item.get("topic") or item.get("tag"))}
            for item in FAQ_FALLBACK_ITEMS[:limit]
        ]

    top_rows = faq_df.sort_values("viewCnt", ascending=False).head(limit)
    items = []
    for _, row in top_rows.iterrows():
        items.append(
            {
                "title": row["title"],
                "topic": row.get("symptom_category") or "FAQ",
                "tag": row.get("symptom_category") or "FAQ",
                "topic_key": topic_to_icon_key(row.get("symptom_category") or "FAQ"),
                "content": row.get("cleaned_content") or "선택한 질문에 대한 안내를 준비했습니다.",
            }
        )
    return items


def find_question_detail(question):
    if not question:
        items = load_popular_question_items(limit=1)
        return items[0] if items else FAQ_FALLBACK_ITEMS[0]

    faq_df = load_faq_data()
    if not faq_df.empty:
        exact = faq_df[faq_df["title"] == question]
        if exact.empty:
            exact = faq_df[faq_df["title"].str.contains(question, case=False, na=False)]
        if not exact.empty:
            row = exact.iloc[0]
            return {
                "title": row["title"],
                "topic": row.get("symptom_category") or "FAQ",
                "tag": row.get("symptom_category") or "FAQ",
                "topic_key": topic_to_icon_key(row.get("symptom_category") or "FAQ"),
                "content": row.get("cleaned_content") or "상세 안내 내용을 준비 중입니다.",
            }

    for item in FAQ_FALLBACK_ITEMS:
        if question in item["title"] or item["title"] in question:
            return {**item, "topic_key": topic_to_icon_key(item.get("topic") or item.get("tag"))}
    fallback = FAQ_FALLBACK_ITEMS[0]
    return {**fallback, "topic_key": topic_to_icon_key(fallback.get("topic") or fallback.get("tag"))}


def find_direct_answer(question):
    normalized = str(question or "").strip()
    if not normalized:
        return None

    faq_df = load_faq_data()
    if not faq_df.empty:
        exact = faq_df[faq_df["title"] == normalized]
        if exact.empty:
            exact = faq_df[faq_df["title"].str.contains(normalized, case=False, na=False)]
        if exact.empty:
            exact = faq_df[faq_df["cleaned_content"].str.contains(normalized, case=False, na=False)]
        if not exact.empty:
            row = exact.iloc[0]
            return (row.get("cleaned_content") or "").strip() or None

    for item in FAQ_FALLBACK_ITEMS:
        title = str(item.get("title") or "")
        content = str(item.get("content") or "").strip()
        if normalized == title or normalized in title or title in normalized:
            return content or None

    return None
