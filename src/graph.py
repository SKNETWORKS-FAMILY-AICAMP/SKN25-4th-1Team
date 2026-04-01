from langgraph.graph import StateGraph, END
from src.state import GraphState

from src.nodes import (
    chat_node,
    retrieve_node,
    nearest_center_node,
    generate_node,
    self_repair_classifier_node,
    ask_intent_node,
    self_repair_guide_node,
    route_question,
    grade_document_routing,
    check_hallucination_routing,
    route_after_self_repair_check
)

def build_cs_rag_graph():
    """LangGraph 기반의 Agentic RAG 파이프라인을 구축합니다."""
    
    # 1. 그래프 초기화 (GraphState 바구니를 들고 다닐 컨베이어 벨트 생성)
    workflow = StateGraph(GraphState)
    
    # ==========================================
    # 2. 노드(작업장) 등록
    # ==========================================
    workflow.add_node("chat_node", chat_node)
    workflow.add_node("retrieve_node", retrieve_node)
    workflow.add_node("nearest_center_node", nearest_center_node)
    workflow.add_node("generate_node", generate_node)
    workflow.add_node("self_repair_classifier_node", self_repair_classifier_node)
    workflow.add_node("ask_intent_node", ask_intent_node)
    workflow.add_node("self_repair_guide_node", self_repair_guide_node)

    # ==========================================
    # 3. edge 연결
    # ==========================================
    
    # [시작점 설정] 질문이 들어오면 가장 먼저 의도를 분류(Router)합니다.
    workflow.set_conditional_entry_point(
        route_question,
        {
            "chat_node": "chat_node",          # 잡담이면 chat_node로 이동
            "retrieve_node": "retrieve_node"   # CS 문의면 검색 노드로 이동
        }
    )

    # [검색 -> 평가 분기] 문서를 찾은 뒤, 이 문서가 쓸만한지 평가합니다.
    workflow.add_conditional_edges(
        "retrieve_node",
        grade_document_routing,
        {
            "generate_node": "generate_node",     
            "nearest_center_node": "nearest_center_node"  # 웹 검색 대신 센터 안내로!
        }
    )
    workflow.add_conditional_edges(
        "generate_node",
        check_hallucination_routing,
        {
            "self_repair_classifier_node": "self_repair_classifier_node", # 정상
            "nearest_center_node": "nearest_center_node"                  # 환각 발견 시
        }
    )

    # [자가수리 판별 -> 최종 분기] 고객의 자가수리 의향 및 대상 여부에 따라 흐름을 가릅니다.
    workflow.add_conditional_edges(
        "self_repair_classifier_node",
        route_after_self_repair_check,
        {
            "self_repair_guide_node": "self_repair_guide_node", # 의향 있음 -> 가이드 병합
            "ask_intent_node": "ask_intent_node",               # 의향 모름 -> 역질문 추가
            "END": END                                          # 대상 아님 -> 생성된 답변 그대로 반환 후 종료
        }
    )

    # ==========================================
    # 4. 종료점(END) 연결
    # ==========================================
    workflow.add_edge("chat_node", END)
    workflow.add_edge("nearest_center_node", END)
    workflow.add_edge("ask_intent_node", END)
    workflow.add_edge("self_repair_guide_node", END)

    # 5. 그래프 컴파일 (실행 가능한 앱 형태로 변환)
    app = workflow.compile()
    
    return app

# 싱글톤 형태로 앱 인스턴스 내보내기
rag_app = build_cs_rag_graph()