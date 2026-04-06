import os
import json
from datetime import datetime
from pymongo import MongoClient
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# [1] MongoDB 설정 (기존 사용 로그용)
# ==========================================
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = None
log_collection = None

try:
    if MONGO_URI:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client["chatbot_db"]
        log_collection = db["usage_logs"]
    else:
        print("[MongoDB Warning] MONGO_URI가 설정되지 않았습니다.")
except Exception as e:
    print(f"[MongoDB Error] MongoDB 연결 실패: {e}")

def save_usage_log(log_data: dict):
    """기존의 전체 파이프라인 사용 로그 저장 (MongoDB)"""
    try:
        if log_collection is not None:
            log_collection.insert_one(log_data)
        else:
            print(f"[Log] MongoDB 미연결. 콘솔 출력: {log_data}")
    except Exception as e:
        print(f"[MongoDB Log Error] 로그 저장 실패: {e}")


# ==========================================
# [2] Redis 설정 (실시간 노드 성능 로그용)
# ==========================================
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

redis_client = None

try:
    redis_client = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    # 연결 테스트
    redis_client.ping()
except Exception as e:
    print(f"[Redis Warning] Redis 연결 실패 (기능 제한됨): {e}")
    redis_client = None

def save_node_perf(trace_id: str, node_name: str, duration: float, metadata: dict = None):
    """노드별 실행 성능 로그 저장 (Redis Streams)"""
    if redis_client is None:
        print(f"[Perf Log] Redis 미연결 ({node_name}): {duration:.4f}s")
        return

    try:
        log_entry = {
            "trace_id": trace_id,
            "node_name": node_name,
            "duration": str(duration),
            "timestamp": datetime.now().isoformat(),
        }
        if metadata:
            log_entry["metadata"] = json.dumps(metadata)
        
        # Redis Stream에 추가 (XADD)
        # node_perf_stream 이라는 이름의 스트림에 데이터 저장
        redis_client.xadd("node_perf_stream", log_entry)
        print(f"[Redis Stream] {node_name} 저장 완료 ({duration:.4f}s)")
    except Exception as e:
        print(f"[Redis Log Error] 스트림 저장 실패: {e}")
