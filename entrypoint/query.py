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
    """LangGraph 라우팅이 정상 작동하는지 확인하기 위한 시나리오 테스트"""
    
    # 다양한 라우팅(분기)을 테스트할 수 있는 질문 세트
    scenarios = [
        {
            "title": "테스트 1: 단순 인사말 (Router -> Chat Node)",
            "query": "안녕! 오늘 날씨 참 좋다. 넌 이름이 뭐야?"
        },
        {
            "title": "테스트 2: 일반 CS 문의 (Router -> Retrieve -> Generate)",
            "query": "노트 어시스트 기능은 어떻게 사용하나요?"
        },
        {
            "title": "테스트 3: 자가수리 대상 + 의향 없음 (Ask Intent Node)",
            "query": "갤럭시 S22 액정이 깨졌어요. 수리비가 얼마인가요?"
        },
        {
            "title": "테스트 4: 자가수리 대상 + 의향 있음 (Guide Node 병합)",
            "query": "갤럭시 S22 후면 유리가 깨졌는데, 내가 직접 부품 사서 수리할래. 방법 알려줘."
        },
        {
            "title": "테스트 5: 문서에 없는 엉뚱한 질문 (Fallback -> Nearest Center Node)",
            "query": "사과폰 15 프로 전원이 갑자기 안 켜져요. 어떻게 고치죠?"
        }
    ]

    print("=" * 60)
    print("🚀 [Agentic RAG 시나리오 테스트 시작]")
    print("=" * 60)

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n\n▶️ [{scenario['title']}]")
        print(f"👤 사용자: {scenario['query']}")
        print("-" * 60)
        
        # 파이프라인 실행
        result = generate_cs_response(scenario['query'])
        
        # 결과 출력
        print(f"🤖 AI 답변:\n{result['answer']}\n")
        print(f"📑 출처: {result['source_document']}")
        print(f"📊 신뢰도: {result['reliability_score']}")
        
        # 자가수리 판별 결과 (내부 State 확인용)
        if result.get('device_model') or result.get('is_hardware_issue'):
            print("\n[🔍 내부 State (자가수리 판별 결과)]")
            print(f" - 추출된 기기명: {result.get('device_model')}")
            print(f" - 하드웨어 파손 여부: {result.get('is_hardware_issue')}")
            print(f" - 자가수리 의향(True/False/None): {result.get('wants_self_repair')}")
            
    print("\n" + "=" * 60)
    print("✅ [테스트 종료] 모든 시나리오 테스트가 완료되었습니다.")
    print("=" * 60)

if __name__ == "__main__":
    # 시나리오 모드 실행
    run_test_scenarios()
    
    # 시나리오 종료 후, 직접 입력해볼 수 있는 대화형 프롬프트 제공
    print("\n💡 직접 질문을 입력해보세요. (종료하려면 'q' 또는 'quit' 입력)")
    while True:
        user_input = input("\n👤 질문 입력: ")
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("테스트를 종료합니다.")
            break
            
        if not user_input.strip():
            continue
            
        result = generate_cs_response(user_input)
        print("-" * 60)
        print(f"🤖 AI 답변:\n{result['answer']}")
        print(f"\n[출처: {result['source_document']} | 신뢰도: {result['reliability_score']}]")
        print("-" * 60)