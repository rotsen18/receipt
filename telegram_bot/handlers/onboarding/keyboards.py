from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegram_bot.handlers.receipts import static_text
from telegram_bot.models import TelegramUser


def make_keyboard_for_start_command(user: TelegramUser) -> ReplyKeyboardMarkup:
    return make_main_menu_keyboard(user)


def make_main_menu_keyboard(user: TelegramUser) -> ReplyKeyboardMarkup:
    receipts = KeyboardButton(text=static_text.list_receipt_text)
    categories = KeyboardButton(text=static_text.categories_list_view_name)
    new_receipt_button = KeyboardButton(text=static_text.receipt_create_button_name)
    buttons = [[receipts, categories]]
    admnin_buttons = [new_receipt_button]
    if user.is_telegram_admin:
        buttons.append(admnin_buttons)
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
