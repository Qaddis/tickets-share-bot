from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
    

def get_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\U00002B05 Влево", callback_data="left"),
        InlineKeyboardButton(text="\U000027A1 Вправо", callback_data="right")]], resize_keyboard=True,)