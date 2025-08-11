from deep_translator import GoogleTranslator
from transliterate import translit
from rapidfuzz import process
from g4f.client import Client

from config import CITIES

def translate(text: str, source: str, target: str) -> str:
    if source == target:
        return text

    translator = GoogleTranslator(source=source, target=target)
    res = translator.translate(text)

    return res

def translate_city(text: str) -> str:
    translated = translit(text, 'ru')

    res, a, b = process.extractOne(translated, CITIES)

    return res

client = Client()
def translate_job(text: str, source: str, target: str) -> str:
    if source == target:
        return text

    content = (
        f'Твоя задача перевести данное слово с языка {source} на язык {target}. '
        f'Ты должен перевести слово, как название профессии. '
        f'Ответь только перевеодом, без объяснений, без вежливости без знаков перпинания.'
        f'Примеры: '
        f'1. Если нужно перевести с ru на en: ввод пользователья "курьер/Уборщик", твой ответ "Cleaner"; '
        f'2. Если нужно перевести с be на ru: ввод пользователья "Прыбіральнік", твой ответ "Уборщик"'
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': content},
            {'role': 'user', 'content': text}
        ],
        web_search=False
    )

    return response.choices[0].message.content