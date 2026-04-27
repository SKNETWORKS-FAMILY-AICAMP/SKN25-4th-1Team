from __future__ import annotations

import json
import uuid
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from frontend.webui.data_loader import get_category_options, load_device_data, load_faq_df
from frontend.webui.services import get_chat_response


WELCOME_MESSAGE = (
    "안녕하세요! 무엇을 도와드릴까요? 기기 모델을 선택하시면 더 정확한 상담이 가능합니다."
)
DEFAULT_DEVICE = "선택하지 않음"
DEFAULT_SERIES = "선택하지 않음"
DEFAULT_VIEW = "chat"
DEFAULT_SORT = "latest"


def _ensure_messages(request: HttpRequest) -> list[dict[str, str]]:
    messages = request.session.get("messages")
    if isinstance(messages, list) and messages:
        return messages

    messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    request.session["messages"] = messages
    return messages


def _ensure_thread_id(request: HttpRequest) -> str:
    thread_id = request.session.get("thread_id")
    if isinstance(thread_id, str) and thread_id:
        return thread_id

    thread_id = str(uuid.uuid4())
    request.session["thread_id"] = thread_id
    return thread_id


def _find_series_for_device(device_data: dict[str, list[str]], selected_device: str) -> str:
    for series, models in device_data.items():
        if selected_device in models:
            return series
    return DEFAULT_SERIES


def _sort_faqs(faq_df, sort_key: str):
    if faq_df.empty:
        return faq_df

    if sort_key == "views":
        return faq_df.sort_values(["viewCnt", "title"], ascending=[False, True])
    if sort_key == "title":
        return faq_df.sort_values(["title", "viewCnt"], ascending=[True, False])

    if faq_df["exposureDate"].notna().any():
        return faq_df.sort_values(["exposureDate", "viewCnt"], ascending=[False, False])
    return faq_df.sort_values(["viewCnt", "title"], ascending=[False, True])


def _serialize_faq_rows(faq_df) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in faq_df.head(15).itertuples(index=False):
        preview = str(row.cleaned_content).strip()
        rows.append(
            {
                "title": row.title,
                "category": row.symptom_category,
                "url": row.url,
                "view_count": row.viewCnt,
                "content_preview": preview[:260] + ("..." if len(preview) > 260 else ""),
            }
        )
    return rows


@require_GET
def dashboard(request: HttpRequest) -> HttpResponse:
    device_data = load_device_data()
    faq_df = load_faq_df().copy()
    categories = get_category_options()

    messages = _ensure_messages(request)
    thread_id = _ensure_thread_id(request)
    selected_device = request.session.get("selected_device", DEFAULT_DEVICE)
    selected_series = request.session.get(
        "selected_series", _find_series_for_device(device_data, selected_device)
    )
    if selected_device == "기타 기기":
        selected_series = "기타"

    current_view = request.GET.get("view", request.session.get("view", DEFAULT_VIEW))
    if current_view not in {"chat", "faq"}:
        current_view = DEFAULT_VIEW
    request.session["view"] = current_view

    selected_category = request.GET.get("category", "")
    if not selected_category and categories:
        selected_category = request.session.get("selected_category", categories[0])
    if selected_category not in categories and categories:
        selected_category = categories[0]
    request.session["selected_category"] = selected_category

    faq_query = request.GET.get("q", "").strip()
    faq_sort = request.GET.get("sort", request.session.get("faq_sort", DEFAULT_SORT))
    request.session["faq_sort"] = faq_sort

    filtered_faq = faq_df
    if selected_category:
        filtered_faq = filtered_faq[filtered_faq["symptom_category"] == selected_category]
    if faq_query:
        title_mask = filtered_faq["title"].str.contains(faq_query, case=False, na=False)
        content_mask = filtered_faq["cleaned_content"].str.contains(faq_query, case=False, na=False)
        filtered_faq = filtered_faq[title_mask | content_mask]
    filtered_faq = _sort_faqs(filtered_faq, faq_sort)

    popular_questions = (
        faq_df.sort_values(["viewCnt", "title"], ascending=[False, True])["title"].head(6).tolist()
        if not faq_df.empty
        else []
    )

    context = {
        "categories": categories,
        "current_view": current_view,
        "device_data": device_data,
        "faq_query": faq_query,
        "faq_rows": _serialize_faq_rows(filtered_faq),
        "faq_sort": faq_sort,
        "messages": messages,
        "popular_questions": popular_questions,
        "selected_category": selected_category,
        "selected_device": selected_device,
        "selected_series": selected_series,
        "series_options": [DEFAULT_SERIES, *device_data.keys(), "기타"],
        "thread_id": thread_id,
        "total_faq_results": len(filtered_faq.index),
    }
    return render(request, "webui/index.html", context)


@require_POST
def chat_api(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)
    question = str(payload.get("question", "")).strip()
    if not question:
        return JsonResponse({"error": "질문을 입력해주세요."}, status=400)

    messages = _ensure_messages(request)
    thread_id = _ensure_thread_id(request)
    selected_device = request.session.get("selected_device", DEFAULT_DEVICE)

    messages.append({"role": "user", "content": question})
    answer = get_chat_response(question, selected_device, thread_id)
    messages.append({"role": "assistant", "content": answer})

    request.session["messages"] = messages
    request.session["view"] = "chat"
    request.session.modified = True

    return JsonResponse(
        {
            "answer": answer,
            "messages": messages,
            "selected_device": selected_device,
        }
    )


@require_POST
def update_device(request: HttpRequest) -> JsonResponse:
    device_data = load_device_data()
    series = request.POST.get("series", DEFAULT_SERIES).strip() or DEFAULT_SERIES
    device = request.POST.get("device", DEFAULT_DEVICE).strip() or DEFAULT_DEVICE

    selected_device = DEFAULT_DEVICE
    selected_series = DEFAULT_SERIES

    if series == "기타":
        selected_series = "기타"
        selected_device = "기타 기기"
    elif series in device_data:
        selected_series = series
        if device in device_data[series]:
            selected_device = device
        elif device_data[series]:
            selected_device = device_data[series][0]

    request.session["selected_series"] = selected_series
    request.session["selected_device"] = selected_device
    request.session.modified = True

    return JsonResponse(
        {
            "selected_device": selected_device,
            "selected_series": selected_series,
        }
    )


@require_POST
def reset_chat(request: HttpRequest) -> JsonResponse:
    request.session["messages"] = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    request.session["thread_id"] = str(uuid.uuid4())
    request.session["view"] = "chat"
    request.session.modified = True

    return JsonResponse({"messages": request.session["messages"]})
