import os
import time
import random
from tasks import add


def clear_console():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS, Linux
        os.system('clear')


def process_task(task_count=1):
    """
    특정 작업을 처리하는 함수.
    """
    tasks =[]
    for _ in range(task_count):
        x = random.randint(1, 100)
        y = random.randint(1, 100)

        result = add.delay(x, y)
        tasks.append(result)

        print(f"✅ 작업 생성됨: Task ID={result.id} (입력값: {x} + {y})")

    return tasks




def run_tasks(tasks):
    """
    Celery 메시지 큐에 쌓인 작업을 1초 간격으로 처리.
    """
    if not tasks:
        print("🚫 처리할 작업이 없습니다. 메시지 큐가 비어 있습니다.")
        return

    print("🔄 작업을 처리합니다...")
    for task in tasks:
        while not task.ready():
            print(f"⏳ Task {task.id}: 처리 중...")

        print(f"✅ Task {task.id}: 완료! 결과: {task.get()}")

    # 모든 작업 처리 완료 후 큐 비우기
    tasks.clear()
    print("🎉 모든 작업이 처리되었습니다.")



def main():
    """
    작업 요청을 계속 대기 & 처리.
    """
    tasks = []  # 생성된 작업들을 추적
    print("🎉 어플리케이션이 실행 중입니다. 종료하려면 'exit'을 입력하세요.")
    print("📋 명령:")
    print(" - 두 정수를 입력하여 작업 생성 (예: 3 5)")
    print(" - 'random <숫자>'를 입력하여 난수 작업 생성 (예: random 100)")
    print(" - 'check'로 작업 상태 확인")
    print(" - 'run'으로 메시지 큐 처리")
    print(" - 'exit'으로 종료")

    while True:
        user_input = input("\n📥 명령 입력: ").strip()
        
        if user_input.lower() == 'exit':  # 종료
            print("👋🏻 어플리케이션을 종료합니다!")
            break
        
        elif user_input.lower() == 'check':  # 작업 상태 확인
            print("🔍 현재 대기 중인 작업 상태:")
            for task in tasks:
                if task.ready():
                    print(f"✅ Task {task.id}: 완료! 결과: {task.get()}")
                else:
                    print(f"⏳ Task {task.id}: 처리 중...")
            continue
        
        elif user_input.lower() == 'run':  # 메시지 큐 처리
            run_tasks(tasks)
            continue
        
        elif user_input.lower().startswith('random'):  # 난수 작업 생성
            try:
                _, count = user_input.split()
                count = int(count)
                new_tasks = process_task(task_count=count)  # 매번 새로운 난수 생성
                tasks.extend(new_tasks)  # 생성된 작업을 추가
            except ValueError:
                print("🚫 'random <숫자>' 형식으로 입력하세요 (예: random 100)")
            continue
        
        try:
            # 입력된 숫자 처리
            x, y = map(int, user_input.split())
            new_tasks = process_task(task_count=1)  # 입력된 값으로 작업 생성
            tasks.extend(new_tasks)  # 생성된 작업을 추가
        except ValueError:
            print("🚫 잘못된 입력입니다. 두 정수를 입력하거나 'random <숫자>'를 입력하세요.")
            continue

if __name__ == "__main__":
    main()