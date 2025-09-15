from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.callbacks.factories import TicketCallbackFactory


stop_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="✅ Сохранить введённые билеты")]],
    resize_keyboard=True,
)

answer_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="✔️ Да"), KeyboardButton(text="✖️ Нет")]],
    resize_keyboard=True,
)

cannot_answer_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Не могу ввести ответ")]], resize_keyboard=True
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⛔ Отмена")]], resize_keyboard=True
)


def save_ticket_kb(ticket_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data=TicketCallbackFactory(
                        action="save", ticket_id=ticket_id
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data=TicketCallbackFactory(
                        action="decline", ticket_id=ticket_id
                    ).pack(),
                ),
            ]
        ]
    )
