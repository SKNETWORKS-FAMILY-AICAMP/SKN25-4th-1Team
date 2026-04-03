import sys
import os
from dotenv import load_dotenv

# 1. 모듈 경로 설정 (src 폴더 접근용)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# 2. 파이프라인 함수 임포트
from src.pipelines.generation_pipeline import generate_cs_response

# 환경 변수 로드
load_dotenv()

def run_test_scenarios():
    scenarios = [
        {
            "title": "테스트 1: 단순 인사말 (Router -> Chat Node)",
            "query": "안녕! 오늘 날씨 참 좋다. 넌 이름이 뭐야?",
            "thread_id": "user_1"
        },
        {
            "title": "테스트 2: 일반 SW CS 문의 (Router -> Retrieve -> Generate)",
            "query": "따뜻해지거나 뜨거워지는 등 발열 현상",
            "thread_id": "user_6"
        }
    ]

    print("=" * 60)
    print("chat node와 소프트웨어 질문 확인")
    print("=" * 60)

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n\n▶️ [{scenario['title']}] - 대화방: {scenario['thread_id']}")
        print(f"👤 사용자: {scenario['query']}")
        print("-" * 60)
        
        # 파이프라인 실행 (thread_id 전달)
        result = generate_cs_response(scenario['query'], thread_id=scenario['thread_id'])
        
        # 결과 출력
        answer = result.get('answer', '답변을 생성하지 못했습니다.')
        source = result.get('source_document', '출처 없음')
        score = result.get('reliability_score', 'N/A')
        
        print(f"🤖 AI 답변:\n{answer}\n")
        print(f"📑 출처: {source} | 📊 신뢰도: {score}")
        
  
            
    print("\n" + "=" * 60)
    print("[테스트 종료] ")
    print("=" * 60)

if __name__ == "__main__":
    # 1. 정해진 시나리오 모드 실행
    run_test_scenarios()
    
    
    # 사용자가 직접 테스트할 때는 동일한 세션 ID를 유지해야 대화가 이어집니다.
    interactive_thread_id = "userdemo" 
    
    while True:
        user_input = input("\n👤 사용자: ")
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("테스트를 종료합니다.")
            break
            
        if not user_input.strip():
            continue
            
        # 동일한 interactive_thread_id를 넘겨주어 이전 맥락과 Flag를 기억하게 함
        result = generate_cs_response(user_input, thread_id=interactive_thread_id)
        
        print("-" * 60)
        print(f"🤖 AI 답변:\n{result.get('answer')}")
        

        print("-" * 60)