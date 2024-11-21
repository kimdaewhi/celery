#!/bin/bash

# 1. Docker Compose로 Redis와 Celery Worker 실행
echo "Starting Docker containers..."
docker-compose up -d --build

# 2. 가상환경 활성화
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    # venv 없으면 종료
    echo "Virtual environment not found. Please create it first!"
    exit 1
fi

# 3. main.py 실행
echo "Running main.py..."
python app/main.py

# 4. 종료 메시지
echo "All done! You can check Docker logs for worker processing."
