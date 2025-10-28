from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.fsm.get import TicketsToGet
from app.functions.get import get_subject

router = Router()

@router.message(Command("get"))
async def cmd_get(msg: Message, state: FSMContext):
    await state.clear()
      
    await msg.answer("Начинаем поиск нужных вам билетов. Введите курс")
      
    await state.set_state(TicketsToGet.course)
