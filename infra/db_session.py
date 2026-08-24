import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # .env 파일의 환경 변수를 로드
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # 연결이 유효한지 확인하는 옵션
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # yield 후 에 db.close()를 호출하여 세션을 종료.
        # return일 경우 세션을 닫지 못하고 함수가 종료됨.
        db.close()