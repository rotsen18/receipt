from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.handlers.receipts.static_text import detail_receipt_text


def make_keyboard_for_receipt(receipt_id: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(detail_receipt_text, callback_data=f'{receipt_id=}'),
    ]]

    return InlineKeyboardMarkup(buttons)
