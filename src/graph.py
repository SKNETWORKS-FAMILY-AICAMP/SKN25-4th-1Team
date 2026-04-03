from langgraph.graph import StateGraph, START, END
from src.state import GraphState

from src.nodes import (
    chat_node,
    retrieve_node,
    generate_node,
    # nearest_center_node,
    # self_repair_classifier_node,
    # ask_intent_node,
    # self_repair_guide_node,
    route_question,
    # check_hallucination_routing,
    # route_after_self_repair_check
)

# 추가로 구현해야 할 라우팅 함수 
def route_issue_type(state):
    pass


def build_cs_rag_graph():
    """LangGraph 기반의 Agentic RAG 파이프라인을 구축합니다."""
    
    # 1. 그래프 초기화 
    workflow = StateGraph(GraphState)
    
    # ==========================================
    # 2. 노드(작업장) 등록
    # ==========================================
    workflow.add_node("chat_node", chat_node)
    workflow.add_node("retrieve_node", retrieve_node)
    workflow.add_node("generate_node", generate_node)
    
    # --- 향후 확장용 노드 (유지) ---
    # workflow.add_node("nearest_center_node", nearest_center_node)
    # workflow.add_node("self_repair_classifier_node", self_repair_classifier_node)
    # workflow.add_node("ask_intent_node", ask_intent_node)
    # workflow.add_node("self_repair_guide_node", self_repair_guide_node)

    # ==========================================
    # 3. 조건부 Edge 연결 (라우팅)
    # ==========================================
    # 💡 [핵심 수정] 라우터가 반환한 문자열이 실제 어떤 노드로 가야 하는지 명시적으로 매핑 (오류 방지)
    workflow.add_conditional_edges(
        START, 
        route_question,
        {
            "chat_node": "chat_node",
            "retrieve_node": "retrieve_node"
        }
    )

    # --- 향후 확장용 조건부 분기 (유지) ---
    # workflow.add_conditional_edges("retrieve_node", route_issue_type, {...})
    # workflow.add_conditional_edges("self_repair_classifier_node", route_after_self_repair_check, {...})
    # workflow.add_conditional_edges("generate_node", check_hallucination_routing, {...})

    # ==========================================
    # 4. 일반 Edge 및 종료점(END) 연결
    # ==========================================
    # 💡 [핵심 수정] 중복 작성된 add_edge를 제거하고 3단계 흐름을 직관적으로 연결
    workflow.add_edge("retrieve_node", "generate_node") # 검색 후엔 무조건 답변 생성으로!
    
    workflow.add_edge("chat_node", END)                 # 일상 대화 끝나면 종료
    workflow.add_edge("generate_node", END)             # 답변 생성 끝나면 종료

    # ==========================================
    # 5. 그래프 컴파일
    # ==========================================
    app = workflow.compile()
    
    return app
# 싱글톤 형태로 앱 인스턴스 내보내기
rag_app = build_cs_rag_graph()