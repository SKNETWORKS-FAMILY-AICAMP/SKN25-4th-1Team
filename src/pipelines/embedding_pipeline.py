# 텍스트 벡터화 모델 로직
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()

def get_vector_store():
    """ChromaDB 물리적 인덱스 저장소 로드"""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    persist_directory = os.getenv("CHROMA_PERSIST_DIR", "../data/vector_store")
    
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="mobile_cs_manuals"
    )
    return vector_store