from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_async_engine('postgresql+asyncpg://ecommerce:patronus@localhost:5432/ecommerce', echo=True)

# типичная форма URL-адреса базы данных для PostgreSQL
# engine = create_engine('postgresql+asyncpg://ecommerce:xxxxxx@localhost:5432/ecommerce')

# SessionLocal = sessionmaker(bind=engine)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass
