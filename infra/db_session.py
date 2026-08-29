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
    autouse=True,
    autocommit=False,
    autoflush=False,
    bind=engine
)

async def get_db():
    async with SessionLocal() as session:
        yield session