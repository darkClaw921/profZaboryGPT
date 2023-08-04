import telebot

def create_keyboard_is_row(rows: list):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    for row in rows:
        keyboard.row(row)
    return keyboard


def create_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Записаться')
    #keyboard.row('Подборка домов')
    return keyboard