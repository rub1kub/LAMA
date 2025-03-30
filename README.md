# LAMA — Анализ конкурентов для малого бизнеса

LAMA — это сервис для анализа конкурентов поблизости и получения персональных рекомендаций по улучшению бизнеса. Идеально подходит для предпринимателей, открывающих или развивающих локальные точки: кофейни, пекарни, салоны и не только.

## 🚀 Возможности
- Анализ ближайших конкурентов в радиусе 3–4 км
- Поиск сайтов, VK, Telegram конкурентов
- Генерация рекомендаций по улучшению бизнеса с помощью ИИ
- Удобная карта для выбора локации
- Стильный, дружелюбный интерфейс с ламой 🦙

## 🛠️ Технологии
- Backend: **Flask**
- Frontend: **HTML + CSS + JS**
- Карты: **Яндекс.Карты API**
- ИИ: **NVIDIA LLaMA API**

## 📦 Установка и запуск

### 🔧 Требования
- Python 3.10+
- API-ключи от Яндекс и NVIDIA (задать в `config.py`)

### 💻 Установка
```bash
# Клонируем проект
git clone https://github.com/rub1kub/LAMA.git
cd LAMA

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 🚀 Запуск
```bash
python app.py
```

Открой в браузере [http://localhost:5000](http://localhost:5000)

## ⚙️ Настройки `config.py`
```python
YANDEX_API_KEY = "ваш_ключ" брать тут: https://developer.tech.yandex.ru/services/12#
LLAMA_API_KEY = "ваш_ключ_от_NVIDIA" брать тут: https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct
TELEGRAM_API_ID = 12345 брать тут: https://my.telegram.org/
TELEGRAM_API_HASH = "..." брать тут: https://my.telegram.org/
VK_ACCESS_TOKEN = "..." брать тут: https://vkhost.github.io/
```

## 🔮 План развития
- История и сохранение анализа по точкам
- Выгрузка PDF-отчета
- Отзывы из 2ГИС, Google, Яндекс
- Георасширение (другие города и страны)

