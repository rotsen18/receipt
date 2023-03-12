from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.handlers.receipts import static_text


def make_keyboard_for_receipt(receipt_id: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            static_text.receipt_view_button_name,
            callback_data=f'{static_text.receipt_view_button_data}{receipt_id}'
        ),
    ]]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_detail_receipt(receipt_id: int, comments_amount: int = 0) -> InlineKeyboardMarkup:
    comments_button = InlineKeyboardButton(
        static_text.comments_list_button_name,
        callback_data=f'{static_text.comments_list_button_data}{receipt_id}'
    )
    add_comment_button = InlineKeyboardButton(
        static_text.comment_create_button_name,
        callback_data=f'{static_text.comment_create_button_data}{receipt_id}'
    )
    edit_button = InlineKeyboardButton(
        static_text.receipt_edit_button_name,
        callback_data=f'{static_text.receipt_edit_button_data}{receipt_id}'
    )
    buttons = [[
        add_comment_button, edit_button
    ]]
    if comments_amount:
        buttons[0].append(comments_button)

    return InlineKeyboardMarkup(buttons)
