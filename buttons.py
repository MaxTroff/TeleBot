from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import DEFAULT_COMMANDS
from api import get_categories

def commands():
    """
    Функция-предоставления кнопок с доступными командами;
    :return: ReplyKeyBoard
    """
    commands_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    commands_list = []
    for elem in DEFAULT_COMMANDS:
        commands_list.append(KeyboardButton(str(elem[0])))
        if len(commands_list) == commands_markup.row_width:
            commands_markup.add(*commands_list)
            commands_list = []
    if commands_list:
        commands_markup.add(*commands_list)
    return commands_markup

def categories_markup():
    """
    Функция-предоставления кнопок с доступными категориями;
    :return: ReplyKeyBoard
    """
    categories_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    for elem in get_categories():
        categories_markup.add(KeyboardButton(str(elem)))
    return categories_markup

def limit_markup():
    """
    Функция-предоставления кнопок с возможными лимитами на вывод товаров;
    :return: ReplyKeyBoard
    """
    limit_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    limit_markup.add('1', '2', '3')
    limit_markup.add('4', '5', '6')
    limit_markup.add('7', '8', '9')
    limit_markup.add('10')
    return limit_markup

def diapason_markup(prices):
    """
    Функция-предоставления кнопок с доступными кастомными диапазонами;
    :return: ReplyKeyBoard
    """
    diapason_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True)
    diapason_list = []
    for elem in range(prices[0], prices[1] + 1):
        for cur_elem in range(elem + 1, prices[1]):
            diapason_list.append('{}, {}'.format(elem, cur_elem))
            if len(diapason_list) == diapason_markup.row_width:
                diapason_markup.add(*diapason_list)
                diapason_list = []
    if diapason_list:
        diapason_markup.add(*diapason_list)
    return diapason_markup

def goods_markup(goods):
    """
    Функция-предоставления кнопок с доступными id товаров;
    :return: ReplyKeyBoard
    """
    goods_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True)
    goods_id = []
    for good in goods:
        goods_id.append(KeyboardButton(str(good[0])))
        if len(goods_id) == goods_markup.row_width:
            goods_markup.add(*goods_id)
            goods_id = []
    if goods_id:
        goods_markup.add(*goods_id)
    return goods_markup