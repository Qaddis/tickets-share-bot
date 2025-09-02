from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


engine = create_async_engine(
    url=settings.DATABASE_URL, echo=(False if settings.MODE == "PROD" else True)
)
