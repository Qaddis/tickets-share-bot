from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("get"))
async def cmd_get(msg:Message):
      pass
