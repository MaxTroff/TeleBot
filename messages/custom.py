from main import bot
from api import go_to_category
import re

def handle_custom(message, category, limit, custom_range) -> None:
    """
    Функция отправки пользователю всех товаров в указанном диапазоне цен в указанном количественном лимите;
    :param message: Message
    :param category: str
    :param custom_range: List
    :param limit: str
    :return: None
    """
    goods_of_category = go_to_category(category)
    name_to_price = {}
    for elem in goods_of_category:
        if 'price' in elem.keys():
            name_to_price[elem['name']] = elem['price']
    sorted_dict = dict(sorted(name_to_price.items(), key=lambda x: x[1]))
    custom_range = custom_range.split(', ')
    if int(custom_range[0]) > int(custom_range[1]):
        custom_range[0], custom_range[1] = custom_range[1], custom_range[0]
    counter = 0
    result = dict()
    for key, value in sorted_dict.items():
        if not value < int(custom_range[0]) and not value > int(custom_range[1]):
            counter += 1
            result[key] = value
        if counter == int(limit):
            break
    if not result:
        bot.send_message(message.from_user.id, 'В указанном диапазоне цен нет ни одного товара')
        return
    final_list = list()
    for key, value in result.items():
        s = '— '.join([key, str(value)])
        s += '$'
        final_list.append(s)
    bot.send_message(message.from_user.id, '\n'.join(final_list))