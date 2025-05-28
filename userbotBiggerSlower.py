from telethon import TelegramClient
from datetime import datetime
import asyncio

# --- CONFIGURATION ---
api_id = 24850651
api_hash = '43613f2fdc2777422c6357a018b00070'
receiver_id = -4944695970  # Куда пересылать результат

keywords = ['нужен электрик', 'ищу электрика', 'требуется электрик''.']
message_check_limit = 5000
search_interval_seconds = 1800  # 30 минут

client = TelegramClient('userbot_session', api_id, api_hash)
last_seen_ids = {}

# --- CORE FUNCTION ---
async def search_in_chats():
    async for dialog in client.iter_dialogs():
        chat_id = dialog.id
        try:
            print(f"🔍 Проверка чата: {dialog.name} ({chat_id})")

            async for message in client.iter_messages(chat_id, limit=message_check_limit):
                if message.id <= last_seen_ids.get(chat_id, 0):
                    break  # уже обработано

                if message.message:
                    matched_keyword = next((k for k in keywords if k in message.message.lower()), None)

                    if matched_keyword:
                        now = datetime.now().strftime("%d.%m.%Y %H:%M")
                        sender = await message.get_sender()

                        # 🔐 Безопасное получение имени отправителя
                        if hasattr(sender, 'first_name') or hasattr(sender, 'last_name'):
                            sender_name = f"{getattr(sender, 'first_name', '')} {getattr(sender, 'last_name', '')}".strip()
                        elif hasattr(sender, 'title'):
                            sender_name = sender.title  # имя канала
                        else:
                            sender_name = 'Неизвестный отправитель'

                        username = f"@{sender.username}" if getattr(sender, 'username', None) else ""
                        chat_name = dialog.name
                        link = f"https://t.me/c/{str(chat_id)[4:]}/{message.id}" if str(chat_id).startswith('-100') else "ссылка недоступна"

                        await client.send_message(
                            receiver_id,
                            f"📩 Обнаружено по ключевому слову:\n\n{message.message}\n\n"
                            f"🧩 Совпадение: {matched_keyword}\n"
                            f"📅 Время: {now}\n"
                            f"👤 Отправитель: {sender_name} {username}\n"
                            f"🔗 Из чата: {chat_name}\n"
                            f"🔗 Ссылка: {link}"
                        )

                last_seen_ids[chat_id] = max(last_seen_ids.get(chat_id, 0), message.id)

        except Exception as e:
            print(f"❌ Ошибка при обходе чата {chat_id}: {e}")

    print(f"✅ Завершён обход в: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

# --- SCHEDULER ---
async def scheduler():
    while True:
        await search_in_chats()
        await asyncio.sleep(search_interval_seconds)

# --- MAIN ---
async def main():
    await client.start()
    print("🤖 Userbot запущен. Идёт поиск по истории сообщений...")
    await scheduler()

client.loop.run_until_complete(main())