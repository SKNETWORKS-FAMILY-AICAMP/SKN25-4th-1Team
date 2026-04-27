import json
import os
from json import JSONDecodeError
from uuid import uuid4

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import AIMessage, HumanMessage


def _latest_ai_message(messages):
    for message in reversed(messages or []):
        if isinstance(message, AIMessage) or getattr(message, "type", "") == "ai":
            return getattr(message, "content", "")
        if isinstance(message, tuple) and len(message) >= 2 and message[0] in {"ai", "assistant"}:
            return str(message[1])
    return ""


def generate_answer(
    user_message,
    *,
    selected_device="선택하지 않음",
    session_id=None,
    latitude=None,
    longitude=None,
):
    if not os.getenv("OPENAI_API_KEY"):
        return (
            "OPENAI_API_KEY가 설정되어 있지 않아 AI 답변을 생성할 수 없습니다.\n"
            "프로젝트 루트의 .env 파일에 OPENAI_API_KEY 값을 추가한 뒤 Django 서버를 다시 실행해 주세요."
        )

    try:
        from src.graph import rag_app

        trace_id = str(uuid4())
        thread_id = session_id or trace_id
        state = {
            "messages": [HumanMessage(content=user_message)],
            "selected_device": selected_device,
            "context": "",
            "source_document": "",
            "reliability_score": 0.0,
            "trace_id": trace_id,
            "device_model": None,
            "is_hardware_issue": False,
            "waiting_for_repair_choice": False,
        }

        if latitude is not None:
            state["latitude"] = latitude
        if longitude is not None:
            state["longitude"] = longitude

        result = rag_app.invoke(
            state,
            config={"configurable": {"thread_id": thread_id}},
        )
        answer = _latest_ai_message(result.get("messages"))
        if answer:
            return answer
    except Exception as exc:
        return (
            "현재 AI 응답을 생성하는 중 문제가 발생했습니다.\n"
            f"관리자 확인용 오류: {exc}"
        )

    return "답변을 생성하지 못했습니다. 잠시 후 다시 시도해 주세요."


@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 가능합니다."}, status=405)

    try:
        data = json.loads(request.body or b"{}")
    except JSONDecodeError:
        return JsonResponse({"error": "JSON 형식이 올바르지 않습니다."}, status=400)

    user_message = str(data.get("message", "")).strip()
    if not user_message:
        return JsonResponse({"error": "message 값이 필요합니다."}, status=400)

    selected_device = str(data.get("selected_device", "선택하지 않음")).strip() or "선택하지 않음"
    session_id = str(data.get("session_id", "")).strip() or None

    answer = generate_answer(
        user_message,
        selected_device=selected_device,
        session_id=session_id,
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )

    return JsonResponse({"answer": answer})
