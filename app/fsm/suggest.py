from aiogram.fsm.state import StatesGroup, State


class SuggestedTickets(StatesGroup):
    ticket = State()
    answer_state = State()
    answer = State()
    subject = State()
    course = State()
