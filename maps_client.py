# maps_client.py
import hashlib
import logging
import requests
import time
import re
import json
from config import YANDEX_API_KEY, YANDEX_SEARCH_URL

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


def yandex_search(query, ll, spn, max_results=10, retries=3, delay=2):
    params = {
        "text": query,
        "type": "biz",
        "lang": "ru_RU",
        "results": max_results,
        "apikey": YANDEX_API_KEY,
        "ll": ll,
        "spn": spn,
        "rspn": 1
    }
    attempt = 0
    while attempt < retries:
        try:
            logging.debug("Яндекс поиск, попытка %d: запрос: %s", attempt + 1, query)
            response = requests.get(YANDEX_SEARCH_URL, params=params)
            logging.debug("Запрос: %s", response.url)
            if response.status_code == 200:
                cleaned = re.sub(r"```json|```", "", response.text).strip()
                data = json.loads(cleaned)
                logging.debug("Яндекс поиск, получены данные: %s", data)
                results = []
                features = data.get("features", [])
                for feature in features:
                    properties = feature.get("properties", {})
                    meta = properties.get("CompanyMetaData", {})
                    results.append({
                        "href": meta.get("url", ""),
                        "title": properties.get("name", ""),
                        "body": meta.get("description", ""),
                        "address": meta.get("address", "")
                    })
                return results
            else:
                logging.warning("Яндекс поиск, код ответа: %s", response.status_code)
        except Exception as e:
            logging.error("Ошибка при Яндекс поиске: %s", e)
        attempt += 1
        time.sleep(delay)
    raise Exception(f"Не удалось выполнить Яндекс поиск после {retries} попыток для запроса: {query}")


def get_nearby_businesses(lat, lon, radius=2000, business_type="кофейня"):
    logging.debug("Запрос бизнесов: lat=%s, lon=%s, радиус=%s, тип=%s", lat, lon, radius, business_type)
    ll = f"{lon},{lat}"
    delta = radius / 111000
    spn = f"{delta:.3f},{delta:.3f}"
    logging.debug("Параметры поиска: ll=%s, spn=%s, query=%s", ll, spn, business_type)
    results = yandex_search(business_type, ll=ll, spn=spn, max_results=10)

    profiles = []
    if results:
        for result in results:
            url = result.get("href", "")
            title = result.get("title", "")
            snippet = result.get("body", "")
            address = result.get("address", "")
            id_val = int(hashlib.md5((title + address).encode()).hexdigest()[:8], 16)
            profiles.append({
                "id": id_val,
                "name": title,
                "url": url,
                "address": address,
                "category": "Business",
                "description": snippet
            })
    logging.debug("Найденные бизнесы: %s", profiles)
    return profiles