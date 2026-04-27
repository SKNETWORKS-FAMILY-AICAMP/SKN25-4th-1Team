from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DEVICE_DATA_PATH = DATA_DIR / "processed" / "self-repair-list.json"
PROCESSED_FAQ_PATH = DATA_DIR / "processed" / "faq" / "faq_data_v4.csv"
RAW_FAQ_CSV_PATH = DATA_DIR / "raw" / "faq_data_v4.csv"
RAW_FAQ_XLSX_PATH = DATA_DIR / "raw" / "raw_data.xlsx"

CATEGORY_ORDER = [
    "전원/배터리/충전",
    "블루투스",
    "멈춤/오류/속도저하",
    "시스템설정",
    "데이터",
    "네트워크/WI-FI",
    "카메라/갤러리",
    "디스플레이",
    "애플리케이션",
    "통화/문자",
    "센서/터치",
    "소리/진동",
    "업데이트",
    "사양/구성",
    "액세서리",
    "이동통신서비스",
    "기타/주의사항",
]

CATEGORY_ALIASES = {
    "전원": "전원/배터리/충전",
    "배터리": "전원/배터리/충전",
    "충전": "전원/배터리/충전",
    "멈춤/오류/재시작": "멈춤/오류/속도저하",
    "데이터이동": "데이터",
    "전화/문자": "통화/문자",
    "이동통신사서비스": "이동통신서비스",
    "사양/구성품": "사양/구성",
}


def _clean_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("_x000D_", "\n").replace("\u200a", " ")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_category(raw_category: Any) -> str:
    raw_text = _clean_text(raw_category)
    if not raw_text:
        return "기타/주의사항"

    if raw_text in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[raw_text]

    split_parts = [part.strip() for part in raw_text.split(" / ") if part.strip()]
    if not split_parts:
        split_parts = [raw_text]

    for part in split_parts:
        normalized = CATEGORY_ALIASES.get(part, part)
        if normalized in CATEGORY_ORDER:
            return normalized

    return CATEGORY_ALIASES.get(raw_text, raw_text)


def _sort_categories(categories: list[str]) -> list[str]:
    order = {name: index for index, name in enumerate(CATEGORY_ORDER)}
    return sorted(categories, key=lambda item: (order.get(item, len(order)), item))


@lru_cache(maxsize=1)
def load_device_data() -> dict[str, list[str]]:
    if not DEVICE_DATA_PATH.exists():
        return {}

    with DEVICE_DATA_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        return {}

    normalized: dict[str, list[str]] = {}
    for series, models in data.items():
        if isinstance(series, str) and isinstance(models, list):
            normalized[series] = [str(model) for model in models]
    return normalized


def _load_processed_faq() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_FAQ_PATH)
    defaults = {
        "symptom_category": "기타/주의사항",
        "title": "",
        "url": "",
        "cleaned_content": "",
        "viewCnt": 0,
        "exposureDate": None,
    }
    for column, default in defaults.items():
        if column not in df.columns:
            df[column] = default

    df["symptom_category"] = df["symptom_category"].map(normalize_category)
    df["title"] = df["title"].fillna("").astype(str)
    df["url"] = df["url"].fillna("").astype(str)
    df["cleaned_content"] = df["cleaned_content"].map(_clean_text)
    df["viewCnt"] = pd.to_numeric(df["viewCnt"], errors="coerce").fillna(0).astype(int)
    df["exposureDate"] = pd.to_datetime(df["exposureDate"], errors="coerce")
    return df[["title", "symptom_category", "url", "viewCnt", "exposureDate", "cleaned_content"]]


def _load_raw_faq() -> pd.DataFrame:
    if RAW_FAQ_CSV_PATH.exists():
        df = pd.read_csv(RAW_FAQ_CSV_PATH)
    elif RAW_FAQ_XLSX_PATH.exists():
        df = pd.read_excel(RAW_FAQ_XLSX_PATH)
    else:
        return pd.DataFrame(
            columns=["title", "symptom_category", "url", "viewCnt", "exposureDate", "cleaned_content"]
        )

    column_map = {
        "제목": "title",
        "카테고리": "raw_category",
        "본문": "cleaned_content",
        "조회수": "viewCnt",
    }
    df = df.rename(columns=column_map)
    if "title" not in df.columns:
        df["title"] = ""
    if "raw_category" not in df.columns:
        df["raw_category"] = "기타/주의사항"
    if "cleaned_content" not in df.columns:
        df["cleaned_content"] = ""
    if "viewCnt" not in df.columns:
        df["viewCnt"] = 0

    df["symptom_category"] = df["raw_category"].map(normalize_category)
    df["title"] = df["title"].fillna("").astype(str)
    df["url"] = ""
    df["cleaned_content"] = df["cleaned_content"].map(_clean_text)
    df["viewCnt"] = pd.to_numeric(df["viewCnt"], errors="coerce").fillna(0).astype(int)
    df["exposureDate"] = pd.NaT
    return df[["title", "symptom_category", "url", "viewCnt", "exposureDate", "cleaned_content"]]


@lru_cache(maxsize=1)
def load_faq_df() -> pd.DataFrame:
    if PROCESSED_FAQ_PATH.exists():
        return _load_processed_faq()
    return _load_raw_faq()


def get_category_options() -> list[str]:
    faq_df = load_faq_df()
    available = [category for category in faq_df["symptom_category"].dropna().astype(str).unique() if category]
    return _sort_categories(available)
