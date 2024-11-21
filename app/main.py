from tasks import add
import time

# 작업을 비동기로 실행
result = add.delay(4, 6)

# 작업 결과 확인
print("Task ID:", result.id)
print("Result Ready?", result.ready())

while not result.ready():
    print("Task is not ready yet, waiting...")
    time.sleep(1)

print("Result :", result.get())