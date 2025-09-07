from aiogram.filters.callback_data import CallbackData


class TicketCallbackFactory(CallbackData, prefix="ticket"):
    action: str
    data: str
