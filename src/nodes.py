from src_pipelines.state import GraphState
from src_pipelines.embedding_pipeline import get_vector_store
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# LLM 출력을 강제하기 위한 Pydantic 모델
class CSResponse(BaseModel):
    answer: str = Field(description="고객의 질문에 대한 친절하고 정확한 답변")
    source_document: str = Field(description="참조한 문서의 제목 또는 ID")
    reliability_score: float = Field(description="답변의 신뢰도 (0.0 ~ 1.0)")

def retrieve_node(state: GraphState) -> GraphState:
    """ChromaDB에서 관련 문서를 검색합니다."""
    print("---NODE: RETRIEVE---")
    question = state["question"]
    vector_store = get_vector_store()
    
    # MMR 검색 적용
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    docs = retriever.invoke(question)
    
    context = "\n\n".join([f"[출처: {doc.metadata.get('title', 'Unknown')}] {doc.page_content}" for doc in docs])
    
    # 상태 업데이트
    return {"context": context}

def generate_node(state: GraphState) -> GraphState:
    """검색된 문서를 바탕으로 Pydantic 규격에 맞는 답변을 생성합니다."""
    print("---NODE: GENERATE---")
    question = state["question"]
    context = state["context"]
    
    if not context.strip():
        return {
            "answer": "해당 내용에 대한 매뉴얼을 찾을 수 없습니다.",
            "source_document": "N/A",
            "reliability_score": 0.0
        }

    llm = ChatOpenAI(temperature=0.0, model="gpt-4-turbo")
    parser = PydanticOutputParser(pydantic_object=CSResponse)
    
    prompt = PromptTemplate(
        template="당신은 스마트폰 기술 지원 전용 AI 상담사입니다.\n"
                 "반드시 아래 제공된 [참조 문서]만을 기반으로 답변하세요.\n"
                 "문서에 없는 내용은 '해당 내용은 매뉴얼에서 찾을 수 없습니다'라고 답변해야 합니다.\n\n"
                 "[참조 문서]\n{context}\n\n"
                 "[고객 질문]\n{question}\n\n"
                 "{format_instructions}",
        input_variables=["context", "question"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    response_data = chain.invoke({"context": context, "question": question})
    
    # Pydantic 파싱 결과를 상태에 업데이트
    return {
        "answer": response_data.answer,
        "source_document": response_data.source_document,
        "reliability_score": response_data.reliability_score
    }