from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer(
        f"""<b>Привет</b>, {msg.from_user.first_name}! 🎉
Тут ты сможешь найти <b>экзаменационные билеты</b> и <b>ответы</b> на них, чтобы легко закрыть сессию 😘
        """
    )

    await msg.answer("Получить помощь по командам - <b>/help</b>")


@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(
        f"""🗒 <b>Доступные команды</b>:
• <b>/get</b> - Получить экзаменационные билеты
• <b>/offer</b> - Загрузить билеты в базу
• <b>/help</b> - Список команд
"""
    )


@router.message(F.text.contains("/"))
async def other_cmd(msg: Message):
    await msg.answer(
        "⛔ <b>Неизвестная команда</b>!\nДля вывода списка доступных команд используйте <b>/help</b>"
    )
