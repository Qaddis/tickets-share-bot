import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.db.queries import init_db

from app.handlers.general import router as general_router
from app.handlers.suggest import router as suggest_router

from app.callbacks.suggest import router as suggest_callbacks
from app.callbacks.restriction import router as restriction_router

from config import settings


bot = Bot(
    token=settings.TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


async def main():
    await init_db()

    dp.include_router(suggest_callbacks)
    dp.include_router(restriction_router)

    dp.include_router(suggest_router)
    dp.include_router(general_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    if settings.MODE != "PROD":
        logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
