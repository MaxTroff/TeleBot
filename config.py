import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
API_BASE_URL = os.getenv('API_BASE_URL')
RAPID_API_HOST = os.getenv('RAPID_API_HOST')
DEFAULT_COMMANDS = [
    ("/start", "Запустить бот"),
    ("/help", "Доступные команды"),
    ("/all", "Доступные товары"),
    ("/low", "Товары с мин. стоимостью"),
    ("/high", "Товары с макс. стоимостью"),
    ("/custom", "Товары из диапазона цен"),
    ("/desc", "Описание товара"),
    ("/photo", "Фотография товара"),
    ("/history", "История запросов")
]
DB_PATH = 'database.db'

def commands_getter():
    """
    Функция, предоставляющая список доступных команд
    :return: List
    """
    result = list()
    for cmd in DEFAULT_COMMANDS:
        result.append('— '.join([cmd[0], cmd[1]]))
    return result