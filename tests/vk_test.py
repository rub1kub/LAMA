import requests
import re
import logging
import demoji

ACCESS_TOKEN = "vk1.a.2sNOZGmp1HJaA9uX2MjrAa340YTp-E2i_wZxIuj0F7XE6ROWbmL85MxrMyyb4JQSzlWf0orF9QSGifOTXWWaeLtDMQPhz6nn7gWEat9JXmGW5iMFo4QgAO1d_F8xijqdbpqbI1WT5ppJrH8G6XXoPAYjMVbxRmQNIjB7ki_Sb9mi41G-6OfUUsxFnDshwb3sDmg8eWvdb8BeVULTvcFAbQ"
VK_API_VERSION = "5.131"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


def get_group_id(group_domain):
    url = "https://api.vk.com/method/groups.getById"
    params = {
        "group_id": group_domain,
        "access_token": ACCESS_TOKEN,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "response" in data:
        return data["response"][0]["id"]
    else:
        logging.error("Ошибка получения ID группы: %s", data)
        return None


def get_posts(group_id, count=10):
    url = "https://api.vk.com/method/wall.get"
    params = {
        "owner_id": -group_id,
        "count": count,
        "access_token": ACCESS_TOKEN,
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


def get_cleaned_vk_posts(group_domain, count=10):
    group_id = get_group_id(group_domain)
    if not group_id:
        return []

    raw_posts = get_posts(group_id, count=count)
    cleaned_posts = [clean_post_text(post) for post in raw_posts]
    logging.info("Получено %d очищенных постов", len(cleaned_posts))
    return cleaned_posts


if __name__ == "__main__":
    domain = "sm_massmedia"  # Замените на username паблика
    posts = get_cleaned_vk_posts(domain, count=10)
    for i, post in enumerate(posts, start=1):
        print(f"\nПост {i}:\n{post}")