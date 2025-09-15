import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from sqlalchemy import delete

from app.db.database import session_factory
from app.db.models import Blacklist

from app.callbacks.factories import RestrictionCallbackFactory
from app.keyboards.restriction import ban_kb, unban_kb


router = Router()

BANNED_TEXT = "\n\n<b>🤡 Пользователь забанен</b>"


@router.callback_query(RestrictionCallbackFactory.filter(F.action == "ban"))
async def ban(callback: CallbackQuery, callback_data: RestrictionCallbackFactory):
    try:
        async with session_factory() as session:
            doomed = Blacklist(id=int(callback_data.user_id))

            session.add(doomed)

            await session.commit()

        await callback.message.edit_text(
            callback.message.html_text + BANNED_TEXT,
            reply_markup=unban_kb(callback_data.user_id),
        )
        await callback.answer(f"Пользователь {callback_data.user_id} забанен")
    except Exception as e:
        logging.error(f"Error with banning user: {e}")

        await callback.answer("Ошибка! Попробуйте ещё раз")


@router.callback_query(RestrictionCallbackFactory.filter(F.action == "unban"))
async def unban(callback: CallbackQuery, callback_data: RestrictionCallbackFactory):
    try:
        async with session_factory() as session:
            await session.execute(
                delete(Blacklist).where(Blacklist.id == int(callback_data.user_id))
            )

            await session.commit()

            await callback.message.edit_text(
                callback.message.html_text.replace(BANNED_TEXT, ""),
                reply_markup=ban_kb(callback_data.user_id),
            )
            await callback.answer(f"Пользователь {callback_data.user_id} разбанен")
    except Exception as e:
        logging.error(f"Error with unbanning user: {e}")

        await callback.answer("Ошибка! Попробуйте ещё раз")
