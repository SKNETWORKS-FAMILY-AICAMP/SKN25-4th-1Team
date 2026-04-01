# FastAPI 서버 구동 로직 (REST API)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph import rag_app

app = FastAPI(title="LangGraph 기반 Mobile CS API")

class QueryRequest(BaseModel):
    question: str

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        # LangGraph 실행 (초기 상태 주입)
        initial_state = {"question": request.question}
        final_state = rag_app.invoke(initial_state)
        
        return {
            "answer": final_state["answer"],
            "source_document": final_state["source_document"],
            "reliability_score": final_state["reliability_score"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))