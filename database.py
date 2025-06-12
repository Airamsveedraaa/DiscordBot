import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.future import select
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres.tmgevmaxplxzuzrkqcps:s85bAQuH%25Pq%24H6c@aws-0-eu-west-2.pooler.supabase.com:6543/postgres"
)

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"statement_cache_size": 0},  # 👈 Esto soluciona el error con pgbouncer
    poolclass=NullPool,
)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class UserExp(Base):
    __tablename__ = "user_exp"

    user_id = Column(String, primary_key=True, index=True)
    exp = Column(Integer, default=0)
    level = Column(Integer, default=1)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_user_exp(user_id: str):
    async with SessionLocal() as session:
        result = await session.execute(select(UserExp).where(UserExp.user_id == user_id))
        user = result.scalars().first()
        if user:
            return user
        else:
            new_user = UserExp(user_id=user_id, exp=0, level=1)
            session.add(new_user)
            await session.commit()
            return new_user

async def set_user_exp(user_id: str, exp: int, level: int):
    async with SessionLocal() as session:
        result = await session.execute(select(UserExp).where(UserExp.user_id == user_id))
        user = result.scalars().first()
        if user:
            user.exp = exp
            user.level = level
        else:
            user = UserExp(user_id=user_id, exp=exp, level=level)
            session.add(user)
        await session.commit()
