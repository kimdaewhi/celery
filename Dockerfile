# Python 기반 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리
WORKDIR /usr/src/app

# Python 의존성 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY app ./app

# 환경 변수 설정 (Redis broker & Backend URL)
ENV CELERY_BROKER_URL=redis://redis:6380/0
ENV CELERY_RESULT_BACKEND=redis://redis:6380/0

# Celery Worker 실행 명령어를 기본 명령으로 설정
CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
