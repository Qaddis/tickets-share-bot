import logging

from sqlalchemy import update, delete

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.db.database import session_factory
from app.db.models import Tickets

from app.callbacks.factories import TicketCallbackFactory


router = Router()


@router.callback_query(TicketCallbackFactory.filter(F.action == "save"))
async def save_ticket(callback: CallbackQuery, callback_data: TicketCallbackFactory):
    try:
        async with session_factory() as session:
            await session.execute(
                update(Tickets)
                .where(Tickets.id == callback_data.ticket_id)
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

        await callback.answer("Ошибка! Попробуйте ещё раз", show_alert=True)


@router.callback_query(TicketCallbackFactory.filter(F.action == "no-answer"))
async def save_without_answer(
    callback: CallbackQuery, callback_data: TicketCallbackFactory
):
    try:
        async with session_factory() as session:
            await session.execute(
                update(Tickets)
                .where(Tickets.id == callback_data.ticket_id)
                .values(is_active=True, answer=None)
            )

            await session.commit()

        await callback.message.edit_text(
            callback.message.html_text + "\n\n<b>✅ Билет сохранён без ответа</b>",
            reply_markup=None,
        )
    except Exception as e:
        logging.error(f"Error with updating ticket status: {e}")

        await callback.answer("Ошибка! Попробуйте ещё раз", show_alert=True)


@router.callback_query(TicketCallbackFactory.filter(F.action == "decline"))
async def decline_ticket(callback: CallbackQuery, callback_data: TicketCallbackFactory):
    try:
        async with session_factory() as session:
            await session.execute(
                delete(Tickets).where(Tickets.id == callback_data.ticket_id)
            )

            await session.commit()

        await callback.message.edit_text(
            callback.message.html_text + "\n\n<b>❌ Билет не был сохранён</b>",
            reply_markup=None,
        )

        await callback.answer("Билет не сохранён")
    except Exception as e:
        logging.error(f"Error with deleting ticket: {e}")

        await callback.answer("Ошибка! Попробуйте ещё раз", show_alert=True)
