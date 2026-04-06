import os
import json
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from src.graph import rag_app

load_dotenv()

### === log 적재 함수 추가
MONGO_URI = os.getenv("MONGO_URI")

try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["chatbot_db"] # 사용할 데이터베이스명 지정
    log_collection = db["usage_logs"] # 기록을 쌓을 로그 컬렉션명
except Exception as e:
    print(f"[MongoDB Error] MongoDB 연결 실패: {e}")
    mongo_client = None

def save_log(log_data: dict):
    try:
        if mongo_client:
            log_collection.insert_one(log_data)
        else:
            print("[Log Error] MongoDB가 연결되지 않아 저장할 수 없습니다.")
    except Exception as e:
        print(f"[MongoDB Log Error] 로그 저장 실패: {e}")


def generate_cs_response(question: str, selected_device: str = "선택하지 않음", thread_id: str = "default_user"): 
    
    config = {"configurable": {"thread_id": thread_id}}
    print(f" [Pipeline Start] 사용자 질문 접수: {question} (사전 선택 기기: {selected_device})")
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "thread_id": thread_id,
        "selected_device": selected_device,
        "question": question,
        "status": "pending"
    }
 
    try:
        result = rag_app.invoke({"messages": [("user", question)], "selected_device": selected_device}, config)
        print("[Pipeline End] 최종 답변 생성 완료")
        
        final_answer = ""
        if result.get("messages"):
            final_answer = result["messages"][-1].content
        
        log_entry.update({
            "status": "success",
            "answer": final_answer,
            "device_model": result.get("device_model", ""),
            "is_hardware_issue": result.get("is_hardware_issue", False),
            "reliability_score": result.get("reliability_score", 0.0)
        })
        save_log(log_entry)
        
        return result
        
    except Exception as e:
        print(f"[Pipeline Error] 그래프 실행 중 오류 발생: {e}")
        
        log_entry.update({
            "status": "error",
            "error_msg": str(e)
        })
        save_log(log_entry)
        
        return 0