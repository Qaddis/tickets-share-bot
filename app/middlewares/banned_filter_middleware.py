from typing import Any, Dict, Callable, Awaitable

from sqlalchemy import select

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.db.database import session_factory
from app.db.models import Blacklist


class BannedFilterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, any],
    ) -> Any:
        target = event.from_user.id

        async with session_factory() as session:
            banned_user = await session.scalar(
                select(Blacklist).where(Blacklist.id == target)
            )

            if banned_user is not None:
                await event.reply("<b>❌ Отклонено</b>.\nВы были забанены")
            else:
                return await handler(event, data)
