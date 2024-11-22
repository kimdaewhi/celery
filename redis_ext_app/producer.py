import redis
import random

redis_client = redis.Redis(host='localhost', port=6380, db=0)

def produce_tasks(task_count=10):
    """
    Redis에 작업 데이터를 추가.
    """
    for _ in range(task_count):
        task_data = f"Task-{random.randint(1000, 9999)}"
        redis_client.lpush('data_queue', task_data)
        print(f"✅ 작업 데이터 추가됨: {task_data}")

if __name__ == "__main__":
    produce_tasks()
