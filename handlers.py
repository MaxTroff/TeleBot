from telebot.types import Message
from peewee import IntegrityError
import re

from models import User, Command, CommandParameters
from loader import bot
from states import States
from config import commands_getter
import script_chooser
from buttons import categories_markup, get_categories, commands


@bot.message_handler(commands=['start', 'hello-world', 'Привет'])
def starter(message: Message) -> None:
    """
    Функция обработки первой команды('/start', '/hello-world', '/Привет'),
    регистрации нового пользователя и добавления истории сообщений в базу данных
    :param message: Message
    :return: None
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    try:
        cur_user = User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
            )
        Command.create(user=cur_user, command=message.text)
        bot.reply_to(message, "Добро пожаловать в менеджер!")
    except IntegrityError:
        bot.reply_to(message, f"Рады снова вас видеть, {username}!")
        Command.create(user=User.get(User.user_id == message.from_user.id), command=message.text)
    finally:
        bot.set_state(message.from_user.id, States.base, message.chat.id)
        handle_help(message)

def is_reg(message):
    """
    Функция проверки пользователя на регистрацию;
    :param message: Message
    :return: None
    """
    if User.get_or_none(User.user_id == message.from_user.id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return False
    return True

@bot.message_handler(state='*', commands=['low', 'high', 'custom', 'all', 'photo', 'desc'])
def command_handler(message: Message) -> None:
    """
    Функция-обработчик основных команд('/low', '/high', '/custom', '/all', '/photo', '/desc') и выбора категории товаров пользователем;
    :param message: Message
    :return: None
    """
    if not is_reg(message):
        return
    cur_user = User.get(User.user_id == message.from_user.id)
    Command.create(user=cur_user, command=message.text)
    bot.send_message(message.from_user.id, 'Выбран режим {command}.\n'
                                           'Выберите категорию из предложенных:\n\n—{categories}'.format(
        command='"{}"'.format(''.join(re.findall(r'\b\w+', message.text))),
        categories='\n—'.join(get_categories())
    ), reply_markup=categories_markup())
    bot.set_state(message.from_user.id, States.category_choosing, message.chat.id)


@bot.message_handler(state='*', commands=['help'])
def handle_help(message: Message) -> None:
    """
    Функция-обработчик команды '/help', запроса и отправки пользователю доступных команд;
    :param message: Message
    :return: None
    """
    if message.text == '/help':
        cur_user = User.get(User.user_id == message.from_user.id)
        Command.create(user=cur_user, command=message.text)
    bot.send_message(message.from_user.id, 'Введите одну из доступных команд:\n{}'.format(
        ';\n'.join(elem for elem in commands_getter())
    ), reply_markup=commands())
    bot.set_state(message.from_user.id, States.base, message.chat.id)


@bot.message_handler(state='*', commands=['history'])
def history_handle(message: Message) -> None:
    """
    Функция-обработчик команды '/history' и предоставления истории последних 10 запросов;
    :param message: Message
    :return: None
    """
    cur_user = User.get(User.user_id == message.from_user.id)
    Command.create(user=cur_user, command=message.text)
    req_history = []
    for com in Command.select().where(Command.user == cur_user).order_by(-Command.request_id).limit(10):
        req_history.append(str(com.command))
    bot.send_message(message.from_user.id, 'Список последних 10 запросов:\n\n{}'.format(
        '\n'.join(req_history)
                  ), reply_markup=commands())
    bot.set_state(message.from_user.id, States.base, message.chat.id)

@bot.message_handler(state=States.category_choosing)
def limit_or_script_chooser(message: Message) -> None:
    """
    Функция-обработчик состояния category_choosing для выбора скрипта либо ввода лимита в зависимости от команды;
    :param message: Message
    :return: None
    """
    script_chooser.limit_or_script_choosing(message)

@bot.message_handler(state=States.custom_range_choosing)
def go_to_custom(message: Message):
    """
    Функция-обработчик состояния custom_range_choosing для перехода к кастомному скрипту;
    :param message: Message
    :return: None
    """
    script_chooser.go_to_custom_script(message)

@bot.message_handler(state=States.limit_choosing)
def go_to_script(message: Message) -> None:
    """
    Функция-обработчик состояния limit_choosing проверки введенного лимита и перехода к скрипту;
    :param message: Message
    :return: None
    """
    if not message.text.isdigit() or 1 > int(message.text) or int(message.text) > 10:
        bot.send_message(message.from_user.id, 'Вы указали неверный лимит. Попробуйте снова!')
        return
    cur_user = User.get(User.user_id == message.from_user.id)
    cur_command = Command.select().where(Command.user == cur_user).order_by(-Command.request_id).limit(1)[0]
    CommandParameters.create(command=cur_command, name='limit', value=message.text)
    custom_range = CommandParameters.get_or_none(command=cur_command, name="cus_range")
    if custom_range:
        custom_range = custom_range.value
    script_chooser.script_choose(
        message=message,
        command=cur_command.command,
        category=CommandParameters.get(command=cur_command, name="category").value,
        limit=message.text,
        custom_range=custom_range)
    bot.set_state(message.from_user.id, States.base, message.chat.id)

@bot.message_handler(state=States.desc_or_photo_choose)
def go_to_desc_or_photo(message: Message) -> None:
    """
    Функция-обработчик состояния desc_or_photo и перехода к скрипту с описанием и фотографиями
    :param message: Message
    :return: None
    """
    script_chooser.go_to_desc_or_photo_script(message)

@bot.message_handler()
def all_message(message: Message) -> None:
    """
    Функция-обработчик всех неизвестных команд
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, 'Не распознаю эту команду(')
    handle_help(message)
