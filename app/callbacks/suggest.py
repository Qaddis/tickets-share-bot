import logging

from sqlalchemy import update, delete

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from app.db.database import session_factory
from app.db.models import Tickets


class TicketCallbackFactory(CallbackData, prefix="ticket"):
    action: str
    data: str


router = Router()


@router.callback_query(TicketCallbackFactory.filter(F.action == "save"))
async def save_ticket(callback: CallbackQuery, callback_data: TicketCallbackFactory):
    try:
        async with session_factory() as session:
            await session.execute(
                update(Tickets)
                .where(Tickets.id == callback_data.data)
                .values(is_active=True)
            )

            await session.commit()

            await callback.message.edit_text(
                callback.message.html_text + "\n\n<b>✅ Билет сохранён</b>",
                reply_markup=None,
            )
            await callback.answer("Билет успешно сохранён")
    except Exception as e:
        logging.error(f"Error with updating ticket status: {e}")

        await callback.answer("Ошибка! Попробуйте ещё раз")


@router.callback_query(TicketCallbackFactory.filter(F.action == "decline"))
async def decline_ticket(callback: CallbackQuery, callback_data: TicketCallbackFactory):
    try:
        async with session_factory() as session:
            await session.execute(
                delete(Tickets).where(Tickets.id == callback_data.data)
            )

            await session.commit()

            await callback.message.edit_text(
                callback.message.html_text + "\n\n<b>❌ Билет не был сохранён</b>",
                reply_markup=None,
            )

            await callback.answer("Билет не сохранён")
    except Exception as e:
        logging.error(f"Error with deleting ticket: {e}")

        await callback.answer("Ошибка! Попробуйте ещё раз")
