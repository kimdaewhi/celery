import redis

# 실행중인 redis Docker Image에 연결해서 read/write 실행 예제

# redis 연결
r = redis.Redis(host='localhost', port=6379, db=0)

# 테스트 Key-Value 설정
r.set('test_key', 'Hello, Redis!')

value = r.get('test_key')
print(value.decode('utf-8'))