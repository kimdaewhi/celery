from celery import Celery
import time
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
from datetime import datetime
import uuid

# Celery Application 설정
app = Celery('tasks', 
            broker='redis://localhost:6380/0',
            backend='redis://localhost:6380/0'
        )


# 주문지 생성 데이터 검증 모델
class OrderScheme(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="주문고유 ID")     # 주문 ID는 어떤 포맷으로 작성해야 보기 좋을까? 그리고 보기 좋아야할까?
    stk_code: str = Field(..., description="종목 코드")
    trade_type: str = Field(..., description="매매 타입 [매수(buy) / 매도(sell)]")
    order_type: str = Field(..., description="주문 타입 [지정가(limit) / 시장가(market)]")

    account_id: str = Field(None, description="계좌 ID")
    count: int = Field(..., description="매매 수량", gt=0)      # 0보다 큰 값만 
    market: str = Field("KS", description="시장 구분 [KS(KOSPI) / KQ(KOSDAQ)]")
    price: Optional[float] = Field(None, description="지정가; 매매가액")
    create_at: datetime = Field(default_factory=datetime.utcnow, description="주문생성일자")

    # 지정가 매매일 때 price항목 필수 체크
    @model_validator
    def validate_price(cls, values):
        if(values['order_type'] == 'limit' and not values.get('price')):
            raise ValueError("지정가 주문일 경우 price 값은 필수입니다.")
        return values


# Annotation 이용한 작업 정의
@app.task
def add(x, y):
    time.sleep(1.5)
    return x + y



# 주문지 생성 task
@app.task
def create_order_book(stk_code: str, trade_type: str, order_type: str, account_id: str, count: int, market: str,  price: Optional[float] = None):
    try:
        order = OrderScheme(
            stk_code=stk_code,
            trade_type=trade_type,
            order_type=order_type,
            price=price,
            count=count,
            account_id=account_id,
            market=market
        )
        # 주문 생성 (실제 처리는 여기에 추가)
        time.sleep(1)  # 처리 시뮬레이션
        print(f"✅ 주문 생성 완료: {order}")

        return order.model_dump()
    except ValidationError as e:
        print(f"🚫 주문 생성 실패: {e}")
        return {"error": str(e)}