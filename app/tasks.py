from celery import Celery
import time
import pydantic

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


@app.task
def create_order_book(stk_code: str):
    return "this is order_book"