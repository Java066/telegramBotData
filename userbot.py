from telethon import TelegramClient, events
from datetime import datetime

# 🔑 Ваши данные
api_id = 24850651
api_hash = '43613f2fdc2777422c6357a018b00070'
receiver_id = -4944695970  # ID группы для пересылки сообщений

# Ключевые фразы для поиска
keywords = ['нужен электрик', 'ищу электрика', 'требуется электрик']

# Инициализация клиента
client = TelegramClient('userbot_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    message = event.message.message.lower()

    # 📟 Логирование ID чата в консоль
    print(f"📟 Chat info — ID: {event.chat_id}, Type: {'group/channel' if event.is_group or event.is_channel else 'private'}")

    if any(keyword in message for keyword in keywords):
        try:
            # 📅 Получаем текущую дату и время
            now = datetime.now()
            formatted_time = now.strftime("%d.%m.%Y %H:%M")

            chat_name = "неизвестный источник"
            message_link = "ссылка недоступна"
            sender_name = "неизвестный пользователь"
            sender_username = ""

            # 📌 Определяем имя чата и ссылку на сообщение
            if event.is_group or event.is_channel:
                chat = await event.get_chat()
                chat_name = chat.title
                if str(chat.id).startswith("-100"):
                    channel_id = str(chat.id)[4:]
                    message_link = f"https://t.me/c/{channel_id}/{event.message.id}"
                elif hasattr(chat, 'username') and chat.username:
                    message_link = f"https://t.me/{chat.username}/{event.message.id}"
            elif event.sender:
                chat_name = f"{event.sender.first_name} (личный чат)"

            # 👤 Получаем имя и username отправителя
            if event.sender:
                sender = await event.get_sender()
                first = sender.first_name or ""
                last = sender.last_name or ""
                username = f"@{sender.username}" if sender.username else ""
                sender_name = f"{first} {last}".strip()
                sender_username = username

            # ✉️ Отправляем сообщение в указанный чат
            await client.send_message(
                receiver_id,
                f"📩 Сообщение найдено:\n\n{event.message.message}\n\n"
                f"📅 Время: {formatted_time}\n"
                f"👤 Отправитель: {sender_name} {sender_username}\n"
                f"🔗 Из чата: {chat_name}\n"
                f"🔗 Ссылка: {message_link}"
            )

        except Exception as e:
            await client.send_message(receiver_id, f"⚠️ Ошибка при обработке:\n{str(e)}")

# ▶️ Запуск userbot'а
print("🤖 Userbot запущен. Ожидание сообщений...")
client.start()
client.run_until_disconnected()