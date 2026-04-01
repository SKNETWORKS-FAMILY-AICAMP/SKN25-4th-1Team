from typing import TypedDict

class GraphState(TypedDict):
    """
    LangGraph의 상태를 정의합니다.
    """
    question: str               # 사용자 질문
    context: str                # ChromaDB에서 검색된 문서 내용
    answer: str                 # LLM이 생성한 답변
    source_document: str        # 참조 문서 출처
    reliability_score: float    # 답변 신뢰도 점수