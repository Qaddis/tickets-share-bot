from aiogram.fsm.state import StatesGroup, State


class TicketsToGet(StatesGroup):
    subject = State()
    course = State()
