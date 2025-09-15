import logging

from aiogram.types import Message

from app.db.database import session_factory
from app.db.models import Tickets

from app.keyboards.suggest import save_ticket_kb
from app.keyboards.restriction import ban_kb

from config import settings


async def send_tickets_to_admin(msg: Message, data: dict):
    tickets = data.get("tickets", [])
    subject = data.get("subject", "Не указан")
    course = data.get("course", "Не указан")

    result = (
        f"✉️ Новые предложенные билеты от пользователя {f'@{msg.from_user.username}' if msg.from_user.username is not None else f'<i>{msg.from_user.first_name}</i>'} (ID: {msg.from_user.id})\n"
        f"<b>Предмет</b>: {subject}\n"
        f"<b>Курс</b>: {course}\n"
    )

    try:
        await msg.bot.send_message(
            settings.ADMIN, result, reply_markup=ban_kb(str(msg.from_user.id))
        )

        tickets_to_send = []

        async with session_factory() as session:
            for ticket_data in tickets:
                question = ticket_data.get("question")
                answer = ticket_data.get("answer")

                new_ticket = Tickets(
                    subject=subject,
                    course=int(course),
                    question=question,
                    answer=answer,
                    is_active=False,
                )

                session.add(new_ticket)

                tickets_to_send.append(new_ticket)

            await session.flush()

            for i, ticket in enumerate(tickets_to_send, 1):
                await msg.bot.send_message(
                    settings.ADMIN,
                    f"""<b>Билет №{i}</b>

<b>Вопрос</b>:
<code>{ticket.question}</code>

<b>Ответ</b>:
<code>{ticket.answer or '---'}</code>
""",
                    reply_markup=save_ticket_kb(str(ticket.id)),
                )

            await session.commit()

        return True
    except Exception as e:
        logging.error(f"Error sending message to admin: {e}")
        return False
