from langgraph.graph import StateGraph, END
from src.state import GraphState
from src.nodes import retrieve_node, generate_node

def build_cs_rag_graph():
    """LangGraph 기반의 RAG 파이프라인을 구축합니다."""
    workflow = StateGraph(GraphState)
    
    # 1. 노드 추가
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    
    # 2. 엣지 연결 (실행 흐름 정의)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    # 3. 그래프 컴파일
    app = workflow.compile()
    return app

# 싱글톤 형태로 앱 인스턴스 제공
rag_app = build_cs_rag_graph()