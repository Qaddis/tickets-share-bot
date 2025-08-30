import logging

from aiogram.types import Message

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
        await msg.bot.send_message(settings.ADMIN, result)

        for i, ticket in enumerate(tickets, 1):
            question = ticket.get("question")
            answer = ticket.get("answer") or "---"

            await msg.bot.send_message(
                settings.ADMIN,
                f"""<b>Билет №{i}</b>

<b>Вопрос</b>:
<code>{question}</code>

<b>Ответ</b>:
<code>{answer}</code>
""",
            )

        return True
    except Exception as e:
        logging.error(f"Error sending message to admin: {e}")
        return False
