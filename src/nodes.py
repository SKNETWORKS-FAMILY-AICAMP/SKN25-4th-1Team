import os
from pydantic import BaseModel, Field
from typing import Literal, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.state import GraphState
from src.pipelines.embedding_pipeline import get_vector_store

# 공통으로 사용할 LLM (정확한 판단을 위해 temperature=0.0 유지)
llm = ChatOpenAI(temperature=0.0, model="gpt-4-turbo")

# ==========================================
# [1] 구조화된 출력(Pydantic) 모델 정의 
# ==========================================
class RouteQuery(BaseModel):
    intent: Literal["greeting", "cs_query"] = Field(
        description="질문이 단순 인사/잡담이면 'greeting', 기기 고장이나 서비스 문의면 'cs_query'"
    )

class GradeDocument(BaseModel):
    is_relevant: Literal["yes", "no"] = Field(
        description="문서가 사용자의 질문을 해결하는 데 관련이 있으면 'yes', 없으면 'no'"
    )

class HallucinationCheck(BaseModel):
    is_grounded: Literal["pass", "fail"] = Field(
        description="답변이 제공된 문서 내용에만 기반했으면 'pass', 지어낸 내용이 있으면 'fail'"
    )

class SelfRepairExtraction(BaseModel):
    device_model: str = Field(description="언급된 기기 모델명 (예: Galaxy S22), 없으면 빈 문자열")
    is_hardware_issue: bool = Field(description="액정 파손, 배터리 교체 등 물리적 하드웨어 수리가 필요한지 여부")
    wants_self_repair: Optional[bool] = Field(description="사용자가 직접 수리하겠다는 의향을 보였으면 True, 아니면 False, 알 수 없으면 None")

# ==========================================
# [2] 조건부 라우팅 함수 (Conditional Edges)
# ==========================================
def route_question(state: GraphState) -> str:
    """(1) 의도 분류: 질문이 잡담인지 CS 문의인지 판별합니다."""
    print("---ROUTING: 의도 분류 중---")
    structured_llm = llm.with_structured_output(RouteQuery)
    result = structured_llm.invoke(state["question"])
    
    if result.intent == "greeting":
        return "chat_node"
    return "retrieve_node"

def grade_document_routing(state: GraphState) -> str:
    """(3) 문서 평가: 검색된 문서가 유용한지 판별하여 우회(Fallback) 여부를 결정합니다."""
    print("---ROUTING: 문서 유효성 평가 중---")
    structured_llm = llm.with_structured_output(GradeDocument)
    
    prompt = f"다음 문서가 질문에 답변하는 데 유용한지 평가하세요.\n질문: {state['question']}\n문서: {state['context']}"
    result = structured_llm.invoke(prompt)
    
    if result.is_relevant == "yes":
        return "generate_node"
    # 문서가 쓸모없으면 웹 검색 대신 '센터 안내 노드'로 보냅니다.
    return "nearest_center_node"

# ==========================================
# 라우터 함수 수정 (check_hallucination_routing)
# ==========================================
def check_hallucination_routing(state: GraphState) -> str:
    """(6) 환각 검증: 생성된 답변이 문서에 기반하는지 검사합니다."""
    print("---ROUTING: 환각(Hallucination) 검증 중---")
    structured_llm = llm.with_structured_output(HallucinationCheck)
    
    prompt = f"문서: {state['context']}\n답변: {state['answer']}\n답변이 문서의 내용에만 근거하고 있습니까?"
    result = structured_llm.invoke(prompt)
    
    if result.is_grounded == "pass":
        return "self_repair_classifier_node" # 통과하면 자가수리 판별 노드로!
    return "nearest_center_node"

def route_after_self_repair_check(state: GraphState) -> str:
    """(7) 자가수리 대상 판별 후 흐름 제어"""
    print("---ROUTING: 자가수리 진행 여부 판단 중---")
    # 예시: 자가수리 지원 모델 리스트
    SELF_REPAIR_MODELS = ["S20", "S21", "S22", "S23", "Z플립"]
    
    model = state.get("device_model", "")
    is_hw = state.get("is_hardware_issue", False)
    intent = state.get("wants_self_repair", None)
    
    is_target_model = any(target in model.upper() for target in [m.upper() for m in SELF_REPAIR_MODELS])
    
    if is_target_model and is_hw:
        if intent is True:
            return "self_repair_guide_node" # 의향 있음 -> 매뉴얼/부품 안내
        elif intent is None:
            return "ask_intent_node"        # 의향 모름 -> 역질문 추가
            
    return "END" # 대상이 아니거나 의향이 없으면 그대로 종료

# ==========================================
# [3] 실제 작업을 수행하는 노드들 (Nodes)
# ==========================================
def chat_node(state: GraphState) -> GraphState:
    """단순 인사나 잡담을 처리합니다."""
    print("---NODE: 일반 대화---")
    response = llm.invoke(f"고객 서비스 어시스턴트로서 친절하게 답해주세요. 질문: {state['question']}")
    return {"answer": response.content, "source_document": "대화형 AI", "reliability_score": 1.0}

def retrieve_node(state: GraphState) -> GraphState:
    """(2) ChromaDB에서 문서를 검색합니다."""
    print("---NODE: 문서 검색---")
    vector_store = get_vector_store()
    docs = vector_store.as_retriever(search_kwargs={"k": 2}).invoke(state["question"])
    context = "\n\n".join([f"[{d.metadata.get('title', 'Unknown')}] {d.page_content}" for d in docs])
    return {"context": context if context else "검색된 문서 없음"}

def nearest_center_node(state: GraphState) -> GraphState:
    """(4) 내부 매뉴얼로 해결할 수 없을 때 오프라인 센터 방문을 유도합니다."""
    print("---NODE: 센터 방문 안내(Fallback) 수행---")
    
    # 바로 최종 답변(answer)을 덮어씌워서 반환합니다.
    fallback_answer = (
        "말씀하신 증상은 온라인 매뉴얼만으로 정확한 진단 및 해결이 어렵습니다. "
        "기기의 정확한 상태 점검을 위해 전문 엔지니어의 확인이 필요합니다.\n\n"
        "[가까운 삼성전자 서비스센터 찾기 및 방문 예약]\n"
        " https://www.samsungsvc.co.kr/reserve/reserveCenter"
    )
    
    # context를 조작할 필요 없이 바로 answer를 반환하도록 설계합니다.
    return {
        "answer": fallback_answer, 
        "source_document": "오프라인 센터 안내",
        "reliability_score": 1.0
    }

def generate_node(state: GraphState) -> GraphState:
    """(5) 검색된 문서를 바탕으로 1차 답변을 생성합니다."""
    print("---NODE: 1차 답변 생성---")
    prompt = f"다음 문서에만 기반해서 고객의 질문에 답하세요.\n문서: {state['context']}\n질문: {state['question']}"
    response = llm.invoke(prompt)
    return {"answer": response.content, "source_document": "내부 매뉴얼", "reliability_score": 0.9}

def self_repair_classifier_node(state: GraphState) -> GraphState:
    """★ 자가수리 대상인지 상태(State)를 분석하고 업데이트합니다."""
    print("---NODE: 자가수리 요소 분석 중---")
    structured_llm = llm.with_structured_output(SelfRepairExtraction)
    result = structured_llm.invoke(state["question"] + "\n기존 답변: " + state["answer"])
    
    return {
        "device_model": result.device_model,
        "is_hardware_issue": result.is_hardware_issue,
        "wants_self_repair": result.wants_self_repair
    }

def ask_intent_node(state: GraphState) -> GraphState:
    """자가수리 대상이지만 고객의 의향을 모를 때 답변에 역질문을 덧붙입니다."""
    print("---NODE: 자가수리 의향 역질문 추가---")
    appended_answer = state["answer"] + "\n\n💡 **[안내] 해당 모델은 고객님께서 직접 부품을 구매하여 수리하실 수 있는 '자가수리 대상 기기'입니다. 자가수리 매뉴얼과 부품 구매처를 안내해 드릴까요?**"
    return {"answer": appended_answer}

def self_repair_guide_node(state: GraphState) -> GraphState:
    """자가수리 의향이 확인되면 공식 가이드 링크를 답변에 병합합니다."""
    print("---NODE: 자가수리 매뉴얼 및 경고문구 병합---")
    guide_text = (
        f"\n\n🛠️ **[{state['device_model']} 자가수리 가이드]**\n"
        "- 정품 부품 구매처: [삼성전자 서비스 소모품샵 링크]\n"
        "- 공식 수리 매뉴얼 PDF: [해당 모델 분해/조립 매뉴얼 링크]\n"
        "⚠️ **주의사항:** 수리 중 발생하는 추가 파손은 무상 수리 대상에서 제외될 수 있으니, "
        "반드시 절연 장갑을 착용하고 안전 수칙을 준수해 주세요."
    )
    return {"answer": state["answer"] + guide_text}