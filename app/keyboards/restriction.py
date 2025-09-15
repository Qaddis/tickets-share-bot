from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.callbacks.factories import RestrictionCallbackFactory


def ban_kb(user_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🅱️ Забанить",
                    callback_data=RestrictionCallbackFactory(
                        action="ban", user_id=user_id
                    ).pack(),
                )
            ]
        ]
    )


def unban_kb(user_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Разбанить",
                    callback_data=RestrictionCallbackFactory(
                        action="unban", user_id=user_id
                    ).pack(),
                )
            ]
        ]
    )
