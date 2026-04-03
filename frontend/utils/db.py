import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# PostgreSQL DB 접속 URL 설정
# (예시: postgresql://사용자명:비밀번호@호스트:포트/DB이름)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/cs_chatbot")

# SQLAlchemy 엔진 및 세션 생성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 통계 분석 및 로그 관리를 위한 ChatLog 테이블 모델 정의
class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String(255), index=True)   # 세션별 대화를 묶기 위해 인덱스 추가
    device = Column(String(100))                  # 기기별 통계를 위한 필드
    role = Column(String(50))                     # 'user' 또는 'assistant'
    content = Column(Text)                        # 대화 내용
    timestamp = Column(DateTime, default=datetime.utcnow) # 발생 시간

# 테이블 자동 생성 (테이블이 이미 존재하면 무시됨)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[Warning] Failed to connect or create table. Please check if PostgreSQL is running and DB_URL is correct: {e}")

def insert_chat_log(thread_id: str, role: str, content: str, device: str = ""):
    """PostgreSQL DB에 새로운 채팅 로그 트랜잭션을 기록합니다."""
    session = SessionLocal()
    try:
        new_log = ChatLog(
            thread_id=thread_id,
            role=role,
            content=content,
            device=device
        )
        session.add(new_log)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[Error] 채팅 로그 저장 실패: {e}")
    finally:
        session.close()
