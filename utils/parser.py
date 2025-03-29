# utils/parser.py
import requests
import re
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

VK_PATTERN = re.compile(r"https?://(www\.)?vk\.com/[A-Za-z0-9_\.]+")
TG_PATTERN = re.compile(r"https?://(t\.me|telegram\.me)/[A-Za-z0-9_]+")


def extract_social_links(url):
    """
    Загружает страницу сайта и извлекает ссылки на VK и Telegram.
    Возвращает словарь с найденными ссылками или пустые строки.
    """
    logging.debug("Парсинг сайта для ссылок: %s", url)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        all_links = [a.get("href") for a in soup.find_all("a", href=True)]

        vk_links = [link for link in all_links if VK_PATTERN.match(link)]
        tg_links = [link for link in all_links if TG_PATTERN.match(link)]

        result = {
            "vk": vk_links[0] if vk_links else "",
            "telegram": tg_links[0] if tg_links else ""
        }
        logging.debug("Найдено: %s", result)
        return result

    except Exception as e:
        logging.error("Ошибка при парсинге сайта %s: %s", url, e)
        return {"vk": "", "telegram": ""}


if __name__ == "__main__":
    test_url = "https://surfcoffee.ru"
    print(extract_social_links(test_url))
