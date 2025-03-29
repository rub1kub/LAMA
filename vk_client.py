# vk_client.py
import logging
import requests
import re
import demoji
import hashlib
from config import VK_API_VERSION, VK_ACCESS_TOKEN

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def get_group_id(group_domain):
    url = "https://api.vk.com/method/groups.getById"
    params = {
        "group_id": group_domain,
        "access_token": VK_ACCESS_TOKEN,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "response" in data:
        group_id = data["response"][0]["id"]
        logging.debug("Получен group_id: %s", group_id)
        if not str(group_id).isdigit():
            logging.error("group_id не является числовым: %s", group_id)
            return None
        return group_id
    else:
        logging.error("Ошибка получения ID группы: %s", data)
        return None

def get_posts(group_id, count=10):
    url = "https://api.vk.com/method/wall.get"
    params = {
        "owner_id": -group_id,
        "count": count,
        "access_token": VK_ACCESS_TOKEN,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "response" in data:
        return [post["text"] for post in data["response"]["items"] if post["text"].strip()]
    else:
        logging.error("Ошибка при получении постов: %s", data)
        return []

def clean_post_text(text):
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\[club\d+\|[^\]]+\]', '', text)
    text = re.sub(r'\[id\d+\|[^\]]+\]', '', text)
    text = demoji.replace(text, '')
    text = text.replace('\xa0', ' ').replace('\u200B', '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_vk_posts(screen_name, count=5):
    screen_name = str(screen_name)
    logging.debug(screen_name)
    # Очистка screen_name от полной ссылки
    screen_name = screen_name.strip()
    screen_name = re.sub(r'https?://vk\.com/', '', screen_name)
    screen_name = re.sub(r'https?://vk\.ru/', '', screen_name)
    logging.debug("Получение VK постов для: %s", screen_name)
    if not isinstance(screen_name, str) or screen_name.isdigit():
        logging.error("screen_name должен быть username (строкой), а не числовым id: %s", screen_name)
        return []
    group_id = get_group_id(screen_name)
    if not group_id:
        return []
    raw_posts = get_posts(group_id, count=count)
    cleaned_posts = [clean_post_text(post) for post in raw_posts]
    logging.info("Получено очищенных постов: %d", len(cleaned_posts))
    return [{"content": post} for post in cleaned_posts]