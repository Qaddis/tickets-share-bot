from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
