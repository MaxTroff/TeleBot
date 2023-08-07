import requests
from typing import List
from telebot import types

from config import API_BASE_URL, RAPID_API_KEY, RAPID_API_HOST


def api_request(endpoint: str, headers={}) -> requests.Response:
    headers["X-RapidAPI-Key"] = RAPID_API_KEY
    headers["X-RapidAPI-Host"] = RAPID_API_HOST
    return requests.get(
        f'{API_BASE_URL}/{endpoint}',
        headers=headers,
    )

def get_deserts() -> List:
    response = api_request('desserts')
    deserts = response.json()
    return deserts

def get_beverages() -> List:
    response = api_request('beverages')
    beverages = response.json()
    return beverages

def get_desert_by_id(id):
    responce = api_request(f'desserts/{id}')
    desert = responce.json()
    return desert

def get_beverage_by_id(id):
    responce = api_request(f'beverages/{id}')
    beverage = responce.json()
    return beverage

def get_all_deserts_id_and_names() -> List:
    deserts = [[elem['id'], elem['name']] for elem in get_deserts()]
    return deserts

def get_all_beverages_id_and_names() -> List:
    beverages = [[elem['id'], elem['name']] for elem in get_beverages()]
    return beverages

def get_all_prices(category) -> List:
    if category == 'deserts':
        deserts = [int(elem['price']) for elem in get_deserts() if 'price' in elem.keys()]
        diapason = [min(deserts), max(deserts)]
    else:
        beverages = [int(elem['price']) for elem in get_beverages() if 'price' in elem.keys()]
        diapason = [min(beverages), max(beverages)]
    return diapason


def get_categories() -> List:
    return ['deserts', 'beverages']

def go_to_category(category_name) -> List:
    if category_name == 'beverages':
        return get_beverages()
    return get_deserts()

def go_to_category_id_and_names(category_name) -> List:
    if category_name == 'beverages':
        return get_all_beverages_id_and_names()
    return get_all_deserts_id_and_names()

def go_to_good_by_id(id, category):
    if category == 'beverages':
        return get_beverage_by_id(id)
    return get_desert_by_id(id)

def buttons_getter():
    buttons_list = []
    for category in get_categories():
        button = types.KeyboardButton(category)
        buttons_list.append(button)
    return buttons_list