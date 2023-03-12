from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from telegram_bot.handlers.receipts.static_text import receipt_view_button_name, list_receipt_text


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    return make_main_menu_keyboard()


def make_main_menu_keyboard():
    button1 = KeyboardButton(text=list_receipt_text)
    buttons = [[button1]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
