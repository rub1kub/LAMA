# analysis_client.py
import json
import re
import logging
from openai import OpenAI  # Используем библиотеку openai

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def analyze_business(aggregated_info, api_key=None, temperature=0.5, max_tokens=1024):
    """
    Отправляет агрегированные данные (текущий бизнес + конкуренты) в нейросеть и получает анализ и рекомендации.
    """
    if api_key is None:
        raise Exception("API-ключ для нейросети не задан.")
    
    # Инициализируем клиента с указанием базового URL (для NVIDIA Llama API)
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    prompt = f"""
Ты — опытный бизнес-аналитик, специализирующийся на развитии малого и среднего бизнеса.
Проанализируй данные о текущем бизнесе и о конкурентах, находящихся в радиусе 3-4 км.
Данные:
{json.dumps(aggregated_info, ensure_ascii=False, indent=2)}

Выдели:
- Сильные стороны конкурентов (например, оформление соцсетей, акции, вовлечённость)
- Что можно улучшить в текущем бизнесе
- Конкретные рекомендации (например, добавить сторис с отзывами, запустить акции, оптимизировать меню)

Верни ответ в следующем формате (всё текстом):

ANALYSIS|
[Анализ на 2-5 абзацев]

RECOMMENDATIONS|
- Совет 1
- Совет 2
- Совет 3
...

Обязательно добавляй "|" - это разделители, что читает наш код.
"""
    logging.debug("Промпт для нейросети: %s", prompt)
    
    response = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=1,
        max_tokens=max_tokens,
        stream=False
    )
    final_text = response.choices[0].message.content.strip()
    logging.debug("Сырой ответ от нейросети: %s", final_text)
    final_text = final_text.replace("```", "").replace("“", '"').replace("”", '"')
    try:
        final_text = final_text.replace("**ANALYSIS** |", "ANALYSIS|").replace("**RECOMMENDATIONS** |", "RECOMMENDATIONS|")
        analysis_part = ""
        recommendations_part = []
        parts = final_text.split("RECOMMENDATIONS|")
        if len(parts) == 2:
            analysis_part = parts[0].replace("ANALYSIS|", "").strip()
            recommendations_part = [line.strip("- ").strip() for line in parts[1].strip().splitlines() if line.strip()]
        else:
            logging.error("Ответ не содержит разделителя RECOMMENDATIONS|")
        
        parsed = {
            "analysis": analysis_part,
            "recommendations": recommendations_part
        }
        logging.debug("Распарсенный ответ от нейросети: %s", parsed)
        return parsed
    except Exception as e:
        logging.error("Ошибка парсинга ответа от нейросети: %s", e)
        raise e