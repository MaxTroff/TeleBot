from telebot.handler_backends import State, StatesGroup

class States(StatesGroup):
    """
    Дочерний класс с состояниями;
    Родитель: StatesGroup;
    """
    base = State()
    category_choosing = State()
    limit_choosing = State()
    custom_range_choosing = State()
    desc_or_photo_choose = State()
    length = None