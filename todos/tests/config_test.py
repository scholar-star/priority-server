import os

from dotenv import load_dotenv
import pytest

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from infra.priority_db import Base

load_dotenv()

password = os.getenv("TEST_DATABASE_PASSWORD")
TEST_DATABASE_URL = f"postgresql+asyncpg://test_admin:{password}@localhost:5433/priority_db_test"

engine = create_async_engine(
    TEST_DATABASE_URL
)

test_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 모든 테이블 생성

    async with test_session() as session:
        yield session  # 테스트 함수에 세션 제공

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # 모든 테이블 삭제

    await engine.dispose()  # 엔진 종료