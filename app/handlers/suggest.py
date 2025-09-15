from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.fsm.suggest import SuggestedTickets

from app.functions.suggest import send_tickets_to_admin

from app.keyboards.suggest import stop_kb, answer_kb, cannot_answer_kb, cancel_kb


router = Router()


@router.message(Command("suggest"))
async def cmd_suggest(msg: Message, state: FSMContext):
    await state.clear()
    await state.update_data(tickets=[])

    await msg.answer(
        "💻 <b>Окей, начинаем ввод билетов</b>.\nОтправьте <u>текст первого билета</u>",
        reply_markup=cancel_kb,
    )

    await state.set_state(SuggestedTickets.ticket)


@router.message(SuggestedTickets.ticket, F.text == "⛔ Отмена")
async def cancel_proc(msg: Message, state: FSMContext):
    await msg.answer(
        "⛔ <b>Процесс прерван</b>",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()


@router.message(SuggestedTickets.ticket, F.text == "✅ Сохранить введённые билеты")
async def process_stop(msg: Message, state: FSMContext):
    await msg.answer(
        "📝 <b>Ввод билетов завершен</b>.\nТеперь введите <u>название предмета</u>",
        reply_markup=cancel_kb,
    )
    await state.set_state(SuggestedTickets.subject)


@router.message(SuggestedTickets.ticket, F.text)
async def process_ticket(msg: Message, state: FSMContext):
    data = await state.get_data()
    tickets = data.get("tickets", [])

    tickets.append({"question": msg.text.strip(), "answer": None})

    await state.update_data(tickets=tickets)

    await msg.answer(
        f"🗒 Билет №{len(tickets)} <b>принят</b>. Текст:\n<code>{msg.text.strip()}</code>\n\nМожете указать <b>ответ</b> на этот билет?",
        reply_markup=answer_kb,
    )

    await state.set_state(SuggestedTickets.answer_state)


@router.message(SuggestedTickets.answer_state, F.text == "✔️ Да")
async def process_no_answer(msg: Message, state: FSMContext):
    await msg.answer(
        "✔️ Отлично.\nВведите <u>ответ</u> на указанный ранее билет",
        reply_markup=cannot_answer_kb,
    )

    await state.set_state(SuggestedTickets.answer)


@router.message(SuggestedTickets.answer_state, F.text == "✖️ Нет")
@router.message(SuggestedTickets.answer_state, F.text)
async def process_yes_answer(msg: Message, state: FSMContext):
    await msg.answer(
        '✖️ Хорошо.\nВведите <u>текст</u> следующего билета или нажмите <b>"✅ Сохранить введённые билеты"</b>',
        reply_markup=stop_kb,
    )

    await state.set_state(SuggestedTickets.ticket)


@router.message(SuggestedTickets.answer, F.text == "❌ Не могу ввести ответ")
async def process_cannot_answer(msg: Message, state: FSMContext):
    await msg.answer(
        '❌ <b>Ответ не был сохранен</b>.\nВведите текст следующего билета или нажмите "✅ Сохранить введённые билеты"',
        reply_markup=stop_kb,
    )

    await state.set_state(SuggestedTickets.ticket)


@router.message(SuggestedTickets.answer, F.text)
async def process_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    tickets = data.get("tickets", [])

    if tickets:
        tickets[-1]["answer"] = msg.text.strip()

        await state.update_data(tickets=tickets)

    await msg.answer(
        '✏️ <b>Ответ принят</b>.\nВведите <u>текст</u> следующего билета или нажмите <b>"✅ Сохранить введённые билеты"</b>',
        reply_markup=stop_kb,
    )

    await state.set_state(SuggestedTickets.ticket)


@router.message(SuggestedTickets.subject, F.text == "⛔ Отмена")
async def process_cancel_subject(msg: Message, state: FSMContext):
    await msg.answer(
        "⛔ <b>Процесс прерван</b>",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()


@router.message(SuggestedTickets.subject, F.text)
async def process_subject(msg: Message, state: FSMContext):
    await state.update_data(subject=msg.text.strip())

    await msg.answer(
        "✅ <b>Название предмета сохранено</b>.\nТеперь введите <u>номер курса</u> (например, 1)",
        reply_markup=cancel_kb,
    )

    await state.set_state(SuggestedTickets.course)


@router.message(SuggestedTickets.course, F.text == "⛔ Отмена")
async def process_cancel_course(msg: Message, state: FSMContext):
    await msg.answer(
        "⛔ <b>Процесс прерван</b>",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()


@router.message(SuggestedTickets.course, F.text.isdigit())
async def process_course(msg: Message, state: FSMContext):
    await state.update_data(course=msg.text.strip())

    data = await state.get_data()

    if await send_tickets_to_admin(msg, data):
        await msg.answer(
            "✅ <b>Все билеты успешно отправлены!</b>\nВ ближайшее время администраторы проверят их и загрузят в базу",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await msg.answer(
            "❌ <b>Произошла ошибка при отправке билетов</b>\nПопробуйте позже",
            reply_markup=ReplyKeyboardRemove(),
        )

    await state.clear()


@router.message(SuggestedTickets.course)
async def process_course_invalid(message: Message):
    await message.answer(
        "❌ <b>Номер курса должен быть числом</b>.\nПожалуйста, введите корректный номер курса.",
        reply_markup=cancel_kb,
    )
