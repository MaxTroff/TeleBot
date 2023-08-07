from main import bot
from api import go_to_good_by_id, go_to_category_id_and_names
from buttons import goods_markup

def handle_photo(message, category, good_id):
    """
    Функция отправки пользователю фотографии товара с указанным id из указанной категории;
    :param category: str
    :param message: Message
    :param good_id: str
    :return: None
    """
    good_id = int(good_id)
    goods = go_to_category_id_and_names(category)
    if good_id not in [good[0] for good in goods]:
        bot.send_message(message.from_user.id, 'Введен некорректный id. Попробуйте снова:\n{}'.format(
            '\n'.join('. '.join([str(elem[0]), elem[1]]) for elem in goods)),
                         reply_markup=goods_markup(goods)
                         )
        return
    good = go_to_good_by_id(id=good_id, category=category)
    bot.send_message(message.from_user.id, 'Изображение {}:'.format(good['name']))
    bot.send_photo(message.from_user.id, good['img'][0]['sm'])