from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from telegram_bot.handlers.onboarding.static_text import detail_receipt_text, list_receipt_text


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    return make_menu_keyboard()


def make_keyboard_for_receipt(receipt_id: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(detail_receipt_text, callback_data=f'{receipt_id=}'),
    ]]

    return InlineKeyboardMarkup(buttons)


def make_menu_keyboard():
    button1 = KeyboardButton(text=list_receipt_text)
    buttons = [[button1]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
