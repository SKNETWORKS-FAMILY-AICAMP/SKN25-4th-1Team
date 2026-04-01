# CLI 기반 검색 테스트용

import sys
import os
from dotenv import load_dotenv

from src.pipelines.embedding_pipeline import get_vector_store
load_dotenv()

def test_retriever(query_text: str, top_k: int = 3):
    print(f"\n🔍 [사용자 질문]: '{query_text}'")
    print("=" * 60)
    
    try:
        # 2. Vector DB 인스턴스 가져오기
        vector_store = get_vector_store()
        
        # 3. Retriever 설정 
        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": top_k})
        
        # 4. 문서 검색 실행
        docs = retriever.invoke(query_text)
        
        # 5. 결과 출력
        if not docs:
            print("❌ 관련 문서를 찾을 수 없습니다.")
            return

        for i, doc in enumerate(docs, 1):
            metadata = doc.metadata
            print(f"📄 [검색 결과 {i}]")
            print(f"   - 📁 원본 파일 : {metadata.get('source_file', 'N/A')}")
            print(f"   - 📑 카테고리   : {metadata.get('category', 'N/A')}")
            print(f"   - 📌 문서 제목  : {metadata.get('title', 'N/A')}")
            print(f"   - 👀 조회수     : {metadata.get('views', 0)}")
            
            # 본문 내용이 길 수 있으므로 줄바꿈 처리하여 일부만 출력하거나 전체 출력
            content = doc.page_content.replace('\n', ' ')
            print(f"   - 📝 본문 내용  : {content[:600]}...") 
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ 검색 중 오류 발생: {e}")

if __name__ == "__main__":
    # 테스트해보고 싶은 질문 리스트
    test_queries = [
        "화면 터치가 안 돼요.",
        "알람 설정한 시간에 안 울려요.",
        "노트 어시스트 기능 어떻게 써요?"
    ]
    
    for q in test_queries:
        test_retriever(q, top_k=2)