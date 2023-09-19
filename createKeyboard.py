import telebot

def create_keyboard_is_row(rows: list):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)

    for row in rows:
        keyboard.row(row)
    return keyboard



def create_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Расчет')
    keyboard.row('calc')

    #keyboard.row('Подборка домов')
    return keyboard

def keyboard_quest4():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton(text='0.2mm', callback_data=f"btnDeal_0.2")) 
    keyboard.row(telebot.types.InlineKeyboardButton(text='0.6mm', callback_data=f"btnDeal_0.6")) 
    return keyboard