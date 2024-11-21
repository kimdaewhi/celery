# 개요


## 1. Docker Desktop 및 WSL2 설정
```bash
wsl --list --verbose

# 설정 안되어있으면 wsl2를 기본 버전으로 설정
wsl --set-default-version 2

# docker 커맨드 실행
docker run -d --name redis-celery -p 6379:6379 redis
```
<br/><br/>

## 2. Docker Image 및 Conatiner 생성
![alt text](readmeImgs/image.png)

![alt text](readmeImgs/image-1.png)

Docker 커맨드 라인으로 Redis 연결 테스트
```bash
docker exec -it redis-celery redis-cli

# 접속하면 다음과 같은 프롬프트 표시
127.0.0.1:6379 > PING

# 응답 오면 성공
> PONG
```
<br/><br/>


## 3. Python 앱 이동

### 1. redis 패키지 설치</br>
```bash
pip install redis
```


### 2. redis 서버 연결 테스트
```python
# redis_test.py
import redis

# 실행중인 redis Docker Image에 연결해서 read/write 실행 예제

# redis 연결
r = redis.Redis(host='localhost', port=6379, db=0)

# 테스트 Key-Value 설정
r.set('test_key', 'Hello, Redis!')

value = r.get('test_key')
print(value.decode('utf-8'))
```

### 3. tasks 작성 및 등록
```python
from celery import Celery

# Celery Application 설정
app = Celery('tasks', 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

# Annotation 이용한 작업 정의
@app.task
def add(x, y):
    return x + y
```

```bash
celery -A tasks worker --loglevel=info
```

### 4. main.py 작성 & 실행
```python
from tasks import add

# 작업을 비동기로 실행
result = add.delay(4, 6)

# 작업 결과 확인
print("Task ID:", result.id)
print("Result Ready?", result.ready())
print("Result:", result.get(timeout=10))  # 결과를 기다리며 가져오기
```