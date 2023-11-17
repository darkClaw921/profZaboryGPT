import telebot

def create_keyboard_is_row(rows: list):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    for row in rows:
        keyboard.row(row)
    return keyboard

def create_inlinekeyboard_is_row(rows: dict):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for text, callback in rows.items():
        keyboard.row(telebot.types.InlineKeyboardButton(text=text, callback_data=callback)) 
    return keyboard

def create_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Расчет')
    # keyboard.row('calc')

    #keyboard.row('Подборка домов')
    return keyboard


def keyboard_quest1():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='Профнастил', callback_data=f"type_profNastil")) 
    keyboard.row(telebot.types.InlineKeyboardButton(text='Евроштакетник', callback_data=f"type_evroShtak")) 
    keyboard.row(telebot.types.InlineKeyboardButton(text='Сетка рабица', callback_data=f"type_GridRabit"))
    keyboard.row(telebot.types.InlineKeyboardButton(text='3д забор', callback_data=f"type_3d"))
    keyboard.row(telebot.types.InlineKeyboardButton(text='Жалюзи', callback_data=f"type_Zaluzi"))
    # keyboard.row(telebot.types.InlineKeyboardButton(text='Металлический штакетник', callback_data=f"type_metalSh"))
    return keyboard