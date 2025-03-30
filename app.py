from flask import Flask, request, jsonify, render_template, session
import os
import logging
from analysis_client import analyze_business
from maps_client import get_nearby_businesses
from telegram_client import get_telegram_posts
from vk_client import get_vk_posts
from config import LLAMA_API_KEY
from utils.parser import extract_social_links

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    logging.debug("Отображение главной страницы")
    if 'history' not in session:
        session['history'] = []
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    logging.debug("Получены данные запроса: %s", data)

    lat = data.get("lat")
    lon = data.get("lon")
    business_type = data.get("type", "")
    current_business = data.get("business", {})

    if lat is None or lon is None:
        logging.error("Не указаны координаты")
        return jsonify({"error": "Не указаны координаты"}), 400

    logging.debug("Координаты: lat=%s, lon=%s, тип бизнеса=%s", lat, lon, business_type)

    try:
        nearby_businesses = get_nearby_businesses(lat, lon, radius=2000, business_type=business_type)
        logging.debug("Найдено бизнесов: %d", len(nearby_businesses))
    except Exception as e:
        logging.error("Ошибка получения бизнесов: %s", e)
        return jsonify({"error": "Ошибка получения бизнесов"}), 500

    for business in nearby_businesses:
        url = business.get("url", "")
        social_links = extract_social_links(url)

        vk = social_links.get("vk", "")
        telegram = social_links.get("telegram", "")

        business["vk_posts"] = get_vk_posts(vk) if vk else []
        business["telegram_posts"] = get_telegram_posts(telegram) if telegram else []

    aggregated_info = {
        "current_business": current_business,
        "nearby_businesses": nearby_businesses
    }
    logging.debug("Агрегированная информация: %s", aggregated_info)

    try:
        advice = analyze_business(aggregated_info, LLAMA_API_KEY)
        logging.debug("Рекомендации от нейросети: %s", advice)
    except Exception as e:
        logging.error("Ошибка при анализе бизнеса: %s", e)
        return jsonify({"error": "Ошибка при анализе бизнеса"}), 500

    return jsonify(advice)


@app.route("/competitors", methods=["POST"])
def competitors():
    data = request.get_json()
    logging.debug("Получены данные запроса (competitors): %s", data)

    lat = data.get("lat")
    lon = data.get("lon")
    business_type = data.get("type", "")

    if lat is None or lon is None:
        logging.error("Не указаны координаты")
        return jsonify({"error": "Не указаны координаты"}), 400

    try:
        nearby_businesses = get_nearby_businesses(lat, lon, radius=2000, business_type=business_type)
        logging.debug("Найдено бизнесов: %d", len(nearby_businesses))
    except Exception as e:
        logging.error("Ошибка получения бизнесов: %s", e)
        return jsonify({"error": "Ошибка получения бизнесов"}), 500

    cards = []
    for business in nearby_businesses:
        url = business.get("url", "")
        social_links = extract_social_links(url)
        card = {
            "name": business.get("name", "Без названия"),
            "address": business.get("address", "Адрес неизвестен"),
            "url": url,
            "vk": social_links.get("vk", ""),
            "telegram": social_links.get("telegram", "")
        }
        logging.debug("Карточка конкурента: %s", card)
        cards.append(card)

    logging.debug("Итоговый список карточек: %s", cards)
    return jsonify({"competitors": cards})


if __name__ == "__main__":
    logging.info("Запуск приложения...")
    app.run(debug=True)