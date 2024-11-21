from tasks import process_data

def consume_tasks():
    """
    Celery Consumer: Redis에서 작업을 처리.
    """
    print("🔄 메시지 큐에서 작업을 처리합니다...")
    for _ in range(10):  # 테스트용으로 10개의 작업 처리
        result = process_data.delay()
        print(f"✅ 작업 처리 시작: Task ID={result.id}")

if __name__ == "__main__":
    consume_tasks()
