from main import bot
from api import go_to_category


def handle_high(message, category, limit) -> None:
    """
    Функция отправки пользователю сообщения с выводом максимальных по стоимости товаров
    в указанной категории, ограниченных по количеству введенным лимитом;
    :param category: str
    :param message: Message
    :param limit: str
    :return: None
    """
    goods_of_category = go_to_category(category)
    name_to_price = {}
    for elem in goods_of_category:
        if 'price' in elem.keys():
            name_to_price[elem['name']] = elem['price']
    sorted_dict = dict(sorted(name_to_price.items(), key=lambda x: x[1]))
    counter = 0
    result = dict()
    for key, value in sorted_dict.items():
        counter += 1
        result[key] = value
        if counter == int(limit):
            break
    final_list = list()
    for key, value in result.items():
        s = ': '.join([key, str(value)])
        s += '$'
        final_list.append(s)
    bot.send_message(message.from_user.id, '\n'.join(final_list))