from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from telegram_bot.handlers.receipts import static_text


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    return make_main_menu_keyboard()


def make_main_menu_keyboard():
    receipts = KeyboardButton(text=static_text.list_receipt_text)
    categories = KeyboardButton(text=static_text.categories_list_view_name)
    buttons = [[receipts, categories]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
