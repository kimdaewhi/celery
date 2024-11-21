from celery import Celery
import time

# Celery Application 설정
app = Celery('tasks', 
            broker='redis://localhost:6380/0',
            backend='redis://localhost:6380/0'
        )

# Annotation 이용한 작업 정의
@app.task
def add(x, y):
    time.sleep(1.5)
    return x + y