import logging

from sqlalchemy import select

from aiogram.types import Message

from app.db.database import session_factory
from app.db.models import Tickets

async def get_subject(msg: Message, course: str):
    try:
        subjects = set()
        async with session_factory() as session:
                tickets_result = await session.execute(select(Tickets))
                tickets = tickets_result.scalars().all()
        return tickets
    except Exception as e:
        logging.error(f"Error finding courses: {e}")

        return False