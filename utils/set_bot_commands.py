from telebot.types import BotCommand
from config import DEFAULT_COMMANDS


def set_default_commands(bot) -> None:
    """
    Функция заполнения команд бота по умолчванию
    :param bot: bot
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
