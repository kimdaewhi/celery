from tasks import add
import time

def process_task(x, y):
    """
    특정 작업을 처리하는 함수.
    """
    # Celery 작업을 비동기로 Redis에 추가
    result = add.delay(x, y)

    # 작업 결과 확인
    print("Task ID:", result.id)
    print("Result Ready?", result.ready())

    # 작업 완료 대기
    while not result.ready():
        print("Task 준비되지 않았습니다....대기중입니다.")
        time.sleep(1)

    # 작업 결과 출력
    print("Result:", result.get())


def main():
    """
    작업 요청을 계속 대기하며 처리하는 메인 루프.
    """
    print("어플리케이션이 실행중입니다. 종료하려면 'exit'을 입력하세요.")
    
    while True:
        user_input = input("2개의 정수를 입력하세요 : ").strip()
        
        if user_input.lower() == 'exit':
            print("👋🏻어플리케이션을 종료합니다!")
            break
        
        try:
            # 입력된 숫자 처리
            x, y = map(int, user_input.split())
            process_task(x, y)
        except ValueError:
            print("🚫잘못된 입력입니다. 2개의 정수를 입력하세요")

if __name__ == "__main__":
    main()