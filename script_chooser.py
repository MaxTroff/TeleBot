from messages import low, high, custom, all_goods, photo, description
from loader import bot
from config import commands_getter
from api import go_to_category_id_and_names, get_all_prices, get_categories
from states import States
from buttons import commands, limit_markup, diapason_markup, goods_markup
from models import CommandParameters, Command, User


def script_choose(message, command, category=None, limit=None, custom_range=None) -> None:
    """
    Функция выбора скрипта в соответствии с переданным параметром command;
    :param message: Message
    :param command: str
    :param category: Optional[str]
    :param limit: Optional[str]
    :param custom_range: Optional[List]
    :return: None
    """
    bot.send_message(message.from_user.id, 'Жду ответ сайта...')
    if command == '/low':
        low.handle_low(message=message, category=category, limit=limit)
        bot.set_state(message.from_user.id, States.base, message.chat.id)
    elif command == '/high':
        high.handle_high(message=message, category=category, limit=limit)
        bot.set_state(message.from_user.id, States.base, message.chat.id)
    elif command == '/custom':
        custom.handle_custom(message=message, category=category, limit=limit, custom_range=custom_range)
        bot.set_state(message.from_user.id, States.base, message.chat.id)
    elif command == '/all':
        all_goods.handle_all(message=message, category=category)
        bot.set_state(message.from_user.id, States.base, message.chat.id)
    elif command == '/desc' or command == '/photo':
        id_and_names = go_to_category_id_and_names(category)
        bot.send_message(message.from_user.id, 'Выберите id товара:\n{}'.format(
            '\n'.join('. '.join([str(elem[0]), elem[1]]) for elem in id_and_names)), reply_markup=goods_markup(id_and_names))
        bot.set_state(message.from_user.id, States.desc_or_photo_choose, message.chat.id)
        return
    bot.send_message(message.from_user.id, 'Введите одну из доступных команд:\n{}'.format(
        ';\n'.join(elem for elem in commands_getter())
    ), reply_markup=commands())


def go_to_desc_or_photo_script(message) -> None:
    """
    Функция проверки правильности введенного id товара,
    выбора скрипта с описанием либо с фотографией в соответствии с переданным параметром command;
    :param message: Message
    :return: None
    """
    good_id = message.text
    bot.send_message(message.from_user.id, 'Жду ответ сайта...')
    cur_user = User.get(User.user_id == message.from_user.id)
    cur_command = Command.select().where(Command.user == cur_user).order_by(-Command.request_id).limit(1)[0]
    category = CommandParameters.get(command=cur_command, name="category").value
    if cur_command.command == '/desc':
        description.handle_desc(message, category, good_id)
    else:
        photo.handle_photo(message, category, good_id)
    bot.set_state(message.from_user.id, States.base, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите новую команду:\n{}'.format(
    ';\n'.join(elem for elem in commands_getter())
    ), reply_markup=commands())

def go_to_custom_script(message) -> None:
    """
    Функция проверки введенного диапазона и перехода к введению лимита на кол-во позиций категории;
    :param message: Message
    :return: None
    """
    cus_range = message.text
    cus_range_list = cus_range.split(', ')
    if len(cus_range_list) != 2 or not cus_range_list[0].isdigit() or not cus_range_list[1].isdigit():
        bot.send_message(message.from_user.id, f"Введен неверный диапазон цен! Введите два значения цены в формате: 1, 12 в рамках указанного диапазона:")
        return
    cur_user = User.get(User.user_id == message.from_user.id)
    CommandParameters.create(
        command=Command.select().where(Command.user == cur_user).order_by(-Command.request_id).limit(1)[0],
        name='cus_range',
        value=cus_range)
    bot.send_message(message.from_user.id, f"Введите лимит товаров в указанной категории(не более 10):", reply_markup=limit_markup())
    bot.set_state(message.from_user.id, States.limit_choosing, message.chat.id)

def limit_or_script_choosing(message) -> None:
    """
    Функция проверки категории, ввода диапазона значений либо перехода к кастомному скрипту, скрипту со всеми товарами,
    выбору id позиции для отображения изображения либо описания, либо введению лимита в указанной категории в
    зависимости от введенных значений;
    :param message: Message
    :return: None
    """
    if not message.text in get_categories():
        bot.send_message(message.from_user.id, 'Указана несуществующая категория. Попробуйте снова:')
        return
    cur_user = User.get(User.user_id == message.from_user.id)
    cur_command = Command.select().where(Command.user == cur_user).order_by(-Command.request_id).limit(1)[0]
    category = CommandParameters.create(command=cur_command, name="category", value=message.text)
    if cur_command.command == '/custom':
        bot.send_message(message.from_user.id, 'Жду загрузки списка доступных диапазонов...')
        prices = get_all_prices(category.value)
        bot.send_message(message.from_user.id, 'Введите диапазон значений цен в рамках от {first} до {second} в формате: 1, 7:'.format(
            first=str(prices[0]),
            second=str(prices[1])
        ), reply_markup=diapason_markup(prices))
        bot.set_state(message.from_user.id, States.custom_range_choosing, message.chat.id)
    elif cur_command.command == '/all':
        script_choose(message=message, command=cur_command.command, category=message.text)
    elif cur_command.command == '/photo' or cur_command.command == '/desc':
        script_choose(message=message, command=cur_command.command, category=message.text)
    else:
        bot.send_message(message.from_user.id, f"Введите лимит товаров в указанной категории(не более 10):", reply_markup=limit_markup())
        bot.set_state(message.from_user.id, States.limit_choosing, message.chat.id)