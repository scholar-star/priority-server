import pytest
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import StaticPool
from sqlalchemy.orm import sessionmaker
from infra.priority_db import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # 인메모리 SQLite 데이터베이스 URL

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args = {"check_same_thread": False},  # SQLite의 스레드 체크 비활성화
    poolclass=StaticPool  # 인메모리 데이터베이스를 위한 StaticPool 사용
)

test_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

pytestmark = pytest.mark.asyncio

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 모든 테이블 생성
    yield  # 테스트 실행
    # 인메모리 DB - 테스트 후 테이블 삭제