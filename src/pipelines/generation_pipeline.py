from src.graph import rag_app

def generate_cs_response(query: str) -> dict:
    print(f" [Pipeline Start] 사용자 질문 접수: {query}")
    
    initial_state = {"question": query}
    
    try:
        final_state = rag_app.invoke(initial_state)
        print("[Pipeline End] 최종 답변 생성 완료")
        
        return {
            "answer": final_state.get("answer"),
            "source_document": final_state.get("source_document"),
            "reliability_score": final_state.get("reliability_score"),
            
            "device_model": final_state.get("device_model"),
            "is_hardware_issue": final_state.get("is_hardware_issue", False),
            "wants_self_repair": final_state.get("wants_self_repair")
        }
        
    except Exception as e:
        print(f"[Pipeline Error] 그래프 실행 중 오류 발생: {e}")
        # 시스템 에러 발생 시에도 무너지지 않도록 안전한 기본값 반환
        return {
            "answer": "시스템 내부 오류가 발생했습니다. 잠시 후 다시 시도해주시거나 고객센터로 문의해 주세요.",
            "source_document": "System Error",
            "reliability_score": 0.0,
            "device_model": None,
            "is_hardware_issue": False,
            "wants_self_repair": None
        }