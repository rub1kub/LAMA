# telegram_client.py
import logging
import asyncio
import re
from pyrogram import Client
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

SESSION_NAME = "pyrogram_session"

def get_telegram_posts(channel_username, count=10):
    """
    Получает последние сообщения из Telegram-канала через Pyrogram.
    :param channel_username: Username публичного Telegram-канала
    :param count: Количество сообщений
    :return: Список постов (date + content)
    """
    channel_username = extract_telegram_username(channel_username)
    
    if not isinstance(channel_username, str):
        logging.error("channel_username должен быть строкой (username), а не числовым id")
        return []

    async def fetch():
        app = Client(SESSION_NAME, api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
        await app.start()
        logging.debug("Клиент Telegram (Pyrogram) запущен")
        try:
            posts = []
            async for message in app.get_chat_history(channel_username, limit=count):
                if message.text:
                    posts.append({
                        "date": message.date.isoformat(),
                        "content": message.text
                    })
            logging.info("Получено сообщений: %d", len(posts))
            return posts
        except Exception as e:
            logging.error("Ошибка при получении сообщений из '%s': %s", channel_username, e)
            return []
        finally:
            await app.stop()
            logging.debug("Клиент Telegram остановлен")

    return asyncio.run(fetch())

def extract_telegram_username(url: str) -> str:
    match = re.search(r"t\.me/(@?\w+)", url)
    if match:
        return match.group(1).lstrip("@")
    return ""