from sqlalchemy import text

from app.db.database import engine, Base


async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))

        await conn.run_sync(Base.metadata.create_all)
