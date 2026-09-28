import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import settings

# Database URL, e.g. "sqlite+aiosqlite:///./app.db" or a Postgres URL
DATABASE_URL: str = settings.DATABASE_URL

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,        # Set to True for SQL logging
    future=True,       # Use SQLAlchemy 2.0 style async API
)

# Create a configured "AsyncSession" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)

# Base class for ORM models
Base = declarative_base()

def get_session() -> AsyncSession:
    """
    Async generator dependency to provide a database session.
    Usage example with aiohttp or FastAPI:
        async def endpoint(session: AsyncSession = Depends(get_session)):
            ...
    """
    async def _get():
        async with AsyncSessionLocal() as session:
            yield session
    return _get()