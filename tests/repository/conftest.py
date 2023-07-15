import asyncio
import pytest


@pytest.fixture(scope="session", autouse=True)
async def db():
    from fastapi_skeleton.common.util.database import db

    asyncio.run(db.create_database())

    yield db
    await db._engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def session(db):
    try:
        async with db.async_session_maker() as session:
            yield session
    finally:
        await session.rollback()
        await session.close()
