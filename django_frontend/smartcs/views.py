import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

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
    "안녕하세요. Smart CS입니다. 기기 모델을 선택하고 증상을 입력하면 FAQ, 자가수리, 서비스센터 안내까지 이어서 도와드릴게요."
)


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
    return messages, thread_id, selected_device


@require_GET
def home(request):
    messages, _, selected_device = _get_chat_state(request)
    context = {
        "messages": messages,
        "device_data": load_device_data(),
        "selected_device": selected_device,
        "popular_questions": load_popular_question_items(),
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
def chat_api(request):
    question = request.POST.get("question", "").strip()
    answer_override = request.POST.get("answer_override", "").strip()
    if not question:
        return JsonResponse({"ok": False, "error": "질문을 입력해주세요."}, status=400)

    messages, thread_id, selected_device = _get_chat_state(request)
    messages.append({"role": "user", "content": question})

    answer = answer_override or find_direct_answer(question)
    if not answer:
        answer = chat_with_fastapi(question, selected_device, thread_id)
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
    question = request.GET.get("question", "").strip()
    detail = find_question_detail(question)
    popular_items = load_popular_question_items()
    context = {
        "screen_title": "자주 묻는 질문",
        "question": detail,
        "popular_items": popular_items,
        "topics": [{"name": topic, "key": topic_to_icon_key(topic)} for topic in FAQ_TOPICS],
    }
    return render(request, "smartcs/faq.html", context)


@require_GET
def search(request):
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

    results = faq_df.head(20).to_dict("records") if not faq_df.empty else []
    context = {
        "screen_title": "검색 / 필터",
        "categories": FAQ_CATEGORIES,
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
