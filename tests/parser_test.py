import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def fetch_website_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logging.info("Успешно загружен сайт: %s", url)
        return response.text
    except requests.RequestException as e:
        logging.error("Ошибка при загрузке сайта: %s", e)
        return None

def parse_website_content(html):
    soup = BeautifulSoup(html, "html.parser")
    
    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
    h2_tags = [h2.get_text(strip=True) for h2 in soup.find_all("h2")]
    h3_tags = [h3.get_text(strip=True) for h3 in soup.find_all("h3")]
    h4_tags = [h4.get_text(strip=True) for h4 in soup.find_all("h4")]
    h5_tags = [h5.get_text(strip=True) for h5 in soup.find_all("h5")]
    p_tags = [p.get_text(strip=True) for p in soup.find_all("p")]
    
    logging.info("Найдено заголовков h1: %d", len(h1_tags))
    logging.info("Найдено заголовков h2: %d", len(h2_tags))
    logging.info("Найдено заголовков h3: %d", len(h3_tags))
    logging.info("Найдено заголовков h4: %d", len(h4_tags))
    logging.info("Найдено заголовков h5: %d", len(h5_tags))
    logging.info("Найдено абзацев p: %d", len(p_tags))
    
    return {
        "h1": h1_tags,
        "h2": h2_tags,
        "h3": h3_tags,
        "h4": h4_tags,
        "h5": h5_tags,
        "p": p_tags
    }

if __name__ == "__main__":
    test_url = "https://translate.yandex.ru/"  # Замените на любой нужный сайт
    html = fetch_website_content(test_url)
    if html:
        data = parse_website_content(html)
        print("\n--- Заголовки H1 ---")
        for h in data["h1"]:
            print(f"- {h}")
        
        print("\n--- Заголовки H2 ---")
        for h in data["h2"]:
            print(f"- {h}")

        print("\n--- Заголовки H3 ---")
        for h in data["h3"]:
            print(f"- {h}")

        print("\n--- Заголовки H4 ---")
        for h in data["h4"]:
            print(f"- {h}")

        print("\n--- Заголовки H5 ---")
        for h in data["h5"]:
            print(f"- {h}")
        
        print("\n--- Абзацы P ---")
        for p in data["p"][:5]:  # Ограничим вывод первыми 5
            print(f"- {p}")