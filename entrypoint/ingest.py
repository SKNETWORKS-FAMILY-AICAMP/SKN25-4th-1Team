import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.pipelines.embedding_pipeline import get_vector_store

def ingest_faq_data(file_path: str):
    print(f"[{file_path}] 데이터 로드 시작...")
    
    # 원본 파일명 추출 (경로 제외하고 순수 파일명만)
    file_name = os.path.basename(file_path)
    
    # 1. 데이터 로드 및 전처리 (결측치 빈 문자열 처리)
    try:
        # 파일 확장자에 따라 분기 처리
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            print("❌ 지원하지 않는 파일 형식입니다. (.csv, .xls, .xlsx 만 지원)")
            return
            
        df = df.fillna("") 
    except Exception as e:
        print(f"파일 로드 중 오류 발생: {e}")
        return

    documents = []
    
    # 2. Document 객체 생성 (LLM 친화적인 구조로 텍스트 포매팅)
    for _, row in df.iterrows():
        # 검색 정확도를 높이기 위해 '제목'과 '본문'을 명확히 구분하여 하나로 묶음
        content = (
            f"질문(고객증상): {row.get('제목', '')}\n"
            f"관련 카테고리: {row.get('카테고리', '')}\n"
            f"해결책(가이드): {row.get('본문', '')}"
        )
        
        # 조회수 처리 방어 로직 (문자열 등 예기치 않은 값 대비)
        views_val = str(row.get('조회수', '0'))
        views_int = int(float(views_val)) if views_val.replace('.','',1).isdigit() else 0

        # ChromaDB 메타데이터 (원본 파일명 'source_file' 추가)
        metadata = {
            "source_file": file_name, # 원본 파일 이름 저장
            "source_id": str(row.get('ID', '')),
            "title": str(row.get('제목', '')),
            "category": str(row.get('카테고리', '')),
            "classification": str(row.get('분류', '')),
            "views": views_int
        }
        
        documents.append(Document(page_content=content, metadata=metadata))
        
    print(f"총 {len(documents)}개의 FAQ 데이터를 변환했습니다. 청킹(Chunking)을 진행합니다...")

    # 3. 텍스트 청킹 (Text Splitting)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,       
        chunk_overlap=10,    
        separators=["\n\n", "\n", ".", " ", ""]
    )
    split_docs = text_splitter.split_documents(documents)
    
    # 4. Vector DB (ChromaDB)에 데이터 적재
    print(f"총 {len(split_docs)}개의 청크(Chunk)를 Vector DB에 적재합니다...")
    vector_store = get_vector_store()
    
    # 배치(Batch) 단위 삽입
    batch_size = 150
    for i in range(0, len(split_docs), batch_size):
        batch = split_docs[i : i + batch_size]
        vector_store.add_documents(batch)
        print(f"적재 진행률: {min(i + batch_size, len(split_docs))} / {len(split_docs)}")
        
    print(f"Vector DB(ChromaDB) 구축 완료! (적재된 원본 파일: {file_name})")

if __name__ == "__main__":
    target_file_path = "./data/raw/raw_data.xlsx"
    
    if os.path.exists(target_file_path):
        ingest_faq_data(target_file_path)
    else:
        print(f" 오류: '{target_file_path}' 파일 없음 .")