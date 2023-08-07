from telebot.custom_filters import StateFilter

from models import create_models
from utils.set_bot_commands import set_default_commands
from loader import bot
import handlers



if __name__ == "__main__":
    create_models()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()