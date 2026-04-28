import os
import sys
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from src.utils.translator import translate_to_language

from .data import (
    FAQ_CATEGORIES,
    FAQ_TOPICS,
    find_direct_answer,
    find_question_detail,
    load_device_data,
    load_faq_data,
    load_popular_question_items,
    topic_to_icon_key,
)
from .services import chat_with_fastapi, fetch_nearest_centers, generate_thread_id


DEFAULT_ASSISTANT_MESSAGE = (
    "안녕하세요, Smart CS입니다. 기기 모델을 선택하고 증상을 입력하시면 FAQ, "
    "자가 조치, 서비스센터 안내까지 도와드릴게요."
)

STATIC_HOME_LABELS = {
    "배터리": "Battery",
    "충전": "Charging",
    "와이파이": "Wi-Fi",
    "네트워크": "Network",
    "화면": "Display",
    "디스플레이": "Display",
    "카메라": "Camera",
    "업데이트": "Update",
    "선택하지 않음": "Not selected",
    "기타 기기": "Other device",
}


def _get_chat_state(request):
    messages = request.session.get("messages")
    if not messages:
        messages = [{"role": "assistant", "content": DEFAULT_ASSISTANT_MESSAGE}]
        request.session["messages"] = messages

    thread_id = request.session.get("thread_id")
    if not thread_id:
        thread_id = generate_thread_id()
        request.session["thread_id"] = thread_id

    selected_device = request.session.get("selected_device", "선택하지 않음")
    selected_language = request.session.get("selected_language", "korean")
    return messages, thread_id, selected_device, selected_language


def _is_english_mode(request) -> bool:
    return request.session.get("selected_language", "korean") == "english"


def _translate_display(text: str, use_english: bool) -> str:
    if not text:
        return text
    return translate_to_language(text, "english") if use_english else text


def _translate_home_static_label(text: str, use_english: bool) -> str:
    if not text or not use_english:
        return text

    translated = text
    for source, target in STATIC_HOME_LABELS.items():
        translated = translated.replace(source, target)

    replacements = [
        ("갤럭시", "Galaxy"),
        ("시리즈", "Series"),
        ("폴드", "Fold"),
        ("플립", "Flip"),
        ("울트라", "Ultra"),
        ("플러스", "Plus"),
        ("기본", "Base"),
    ]
    for source, target in replacements:
        translated = translated.replace(source, target)

    return " ".join(translated.split())


def _with_display_fields(item: dict, use_english: bool, field_map: dict) -> dict:
    next_item = dict(item)
    for source_key, display_key in field_map.items():
        next_item[display_key] = _translate_display(str(item.get(source_key, "") or ""), use_english)
    return next_item


@require_GET
def home(request):
    messages, _, selected_device, selected_language = _get_chat_state(request)
    use_english = selected_language == "english"
    raw_device_data = load_device_data()
    device_options = [
        {
            "series": series,
            "display_name": _translate_home_static_label(series, use_english),
            "models": models,
            "display_models": [_translate_home_static_label(model, use_english) for model in models],
        }
        for series, models in raw_device_data.items()
    ]
    popular_questions = [
        {
            **item,
            "display_tag_ko": item.get("tag", ""),
            "display_tag_en": _translate_home_static_label(item.get("tag", ""), True),
            "display_tag": _translate_home_static_label(item.get("tag", ""), use_english),
        }
        for item in load_popular_question_items()
    ]
    context = {
        "messages": messages,
        "device_data": raw_device_data,
        "device_options": device_options,
        "selected_device": selected_device,
        "selected_device_display": _translate_home_static_label(selected_device, use_english),
        "selected_language": selected_language,
        "popular_questions": popular_questions,
        "quick_question": request.GET.get("quick", ""),
        "screen_title": "고객센터",
    }
    return render(request, "smartcs/home.html", context)


@require_GET
def login_view(request):
    return render(request, "smartcs/login.html", {"screen_title": "로그인"})


@require_GET
def signup_view(request):
    return render(request, "smartcs/signup.html", {"screen_title": "회원가입"})


@require_POST
def update_device(request):
    selected_device = request.POST.get("selected_device", "선택하지 않음")
    request.session["selected_device"] = selected_device
    return JsonResponse({"ok": True, "selected_device": selected_device})


@require_POST
def update_language(request):
    selected_language = request.POST.get("selected_language", "korean").strip() or "korean"
    request.session["selected_language"] = selected_language
    request.session.modified = True
    return JsonResponse({"ok": True, "selected_language": selected_language})


@require_POST
def chat_api(request):
    question = request.POST.get("question", "").strip()
    answer_override = request.POST.get("answer_override", "").strip()
    selected_language = request.POST.get("selected_language", "korean").strip() or "korean"
    if not question:
        return JsonResponse({"ok": False, "error": "질문을 입력해 주세요."}, status=400)

    messages, thread_id, selected_device, _ = _get_chat_state(request)
    request.session["selected_language"] = selected_language

    messages.append({"role": "user", "content": question})

    answer = ""
    if selected_language == "english":
        answer = chat_with_fastapi(question, selected_device, thread_id, selected_language)
    else:
        answer = answer_override or find_direct_answer(question)
        if not answer:
            answer = chat_with_fastapi(question, selected_device, thread_id, selected_language)

    messages.append({"role": "assistant", "content": answer})
    request.session["messages"] = messages
    request.session.modified = True

    return JsonResponse({"ok": True, "answer": answer, "messages": messages})


@require_POST
def reset_chat(request):
    request.session["messages"] = [{"role": "assistant", "content": DEFAULT_ASSISTANT_MESSAGE}]
    request.session["thread_id"] = generate_thread_id()
    return JsonResponse({"ok": True})


@require_GET
def faq_browser(request):
    use_english = _is_english_mode(request)
    question = request.GET.get("question", "").strip()
    detail = _with_display_fields(
        find_question_detail(question),
        use_english,
        {
            "title": "display_title",
            "tag": "display_tag",
            "content": "display_content",
        },
    )

    popular_items = [
        _with_display_fields(
            item,
            use_english,
            {
                "title": "display_title",
                "tag": "display_tag",
            },
        )
        for item in load_popular_question_items()
    ]
    topics = [
        {
            "name": topic,
            "display_name": _translate_display(topic, use_english),
            "key": topic_to_icon_key(topic),
        }
        for topic in FAQ_TOPICS
    ]

    context = {
        "screen_title": "자주 묻는 질문",
        "question": detail,
        "popular_items": popular_items,
        "topics": topics,
    }
    return render(request, "smartcs/faq.html", context)


@require_GET
def search(request):
    use_english = _is_english_mode(request)
    faq_df = load_faq_data()
    category = request.GET.get("category", "")
    keyword = request.GET.get("keyword", "").strip()
    sort = request.GET.get("sort", "latest")

    if not faq_df.empty:
        if category:
            faq_df = faq_df[faq_df["symptom_category"] == category]
        if keyword:
            faq_df = faq_df[
                faq_df["title"].str.contains(keyword, case=False, na=False)
                | faq_df["cleaned_content"].str.contains(keyword, case=False, na=False)
            ]

        if sort == "views":
            faq_df = faq_df.sort_values("viewCnt", ascending=False)
        elif sort == "title":
            faq_df = faq_df.sort_values("title")
        else:
            faq_df = faq_df.sort_values("exposureDate", ascending=False)

    raw_results = faq_df.head(20).to_dict("records") if not faq_df.empty else []
    results = [
        {
            **item,
            "display_category": _translate_display(str(item.get("symptom_category", "") or ""), use_english),
            "display_title": _translate_display(str(item.get("title", "") or ""), use_english),
            "display_content": _translate_display(str(item.get("cleaned_content", "") or ""), use_english),
        }
        for item in raw_results
    ]
    categories = [
        {
            "value": category_name,
            "display_name": _translate_display(category_name, use_english),
        }
        for category_name in FAQ_CATEGORIES
    ]

    context = {
        "screen_title": "검색 / 필터",
        "categories": categories,
        "results": results,
        "result_count": len(results),
        "selected_category": category,
        "keyword": keyword,
        "sort": sort,
    }
    return render(request, "smartcs/search.html", context)


def service_centers(request):
    latitude = request.GET.get("lat", "37.5665")
    longitude = request.GET.get("lng", "126.9780")
    try:
        lat_value = float(latitude)
        lng_value = float(longitude)
    except ValueError:
        lat_value = 37.5665
        lng_value = 126.9780

    centers = fetch_nearest_centers(lat_value, lng_value)
    context = {
        "screen_title": "서비스센터 안내",
        "centers": centers,
        "latitude": lat_value,
        "longitude": lng_value,
        "kakao_js_key": os.getenv("KAKAO_MAP_JS_KEY", ""),
    }
    return render(request, "smartcs/service_centers.html", context)
