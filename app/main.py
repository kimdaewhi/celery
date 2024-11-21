from tasks import add

# 작업을 비동기로 실행
result = add.delay(4, 6)

# 작업 결과 확인
print("Task ID:", result.id)
print("Result Ready?", result.ready())
print("Result:", result.get(timeout=10))  # 결과를 기다리며 가져오기