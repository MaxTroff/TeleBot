from main import bot
from api import go_to_category

def handle_all(message, category) -> None:
    """
    Функция отправки пользователю списка всех товаров в указанной категории;
    :param message: Message
    :param category: str
    :return: None
    """
    all_goods = go_to_category(category)
    name_to_price = {}
    name_no_price = {}
    for elem in all_goods:
        if 'price' in elem.keys():
            name_to_price[elem['name']] = elem['price']
        else:
            name_no_price[elem['name']] = '—'
    sorted_dict = dict(sorted(name_to_price.items(), key=lambda x: x[1], reverse=True))
    for key, value in name_no_price.items():
        sorted_dict[key] = value
    final_list = list()
    for key, value in sorted_dict.items():
        s = ': '.join([key, str(value)])
        if value == '—':
            s += ' not available'
        else:
            s += '$;'
        final_list.append(s)
    bot.send_message(message.from_user.id, '\n'.join(final_list))
