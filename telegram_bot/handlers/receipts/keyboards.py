from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.handlers.receipts import static_text
from telegram_bot.models import TelegramUser


def make_keyboard_for_receipt(receipt_id: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            static_text.receipt_view_button_name,
            callback_data=f'{static_text.receipt_view_button_data}{receipt_id}'
        ),
    ]]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_detail_receipt(
    user: TelegramUser,
    receipt_id: int,
    comments_amount: int = 0
) -> InlineKeyboardMarkup:
    comments_button = InlineKeyboardButton(
        static_text.comments_list_button_name,
        callback_data=f'{static_text.comments_list_button_data}{receipt_id}'
    )
    add_comment_button = InlineKeyboardButton(
        static_text.comment_create_button_name,
        callback_data=f'{static_text.comment_create_button_data}{receipt_id}'
    )
    recalculate_button = InlineKeyboardButton(
        static_text.receipt_recalculate_portions_button_name,
        callback_data=f'{static_text.receipt_recalculate_portions_button_data}{receipt_id}'
    )
    all_categories_button = InlineKeyboardButton(
        static_text.receipt_recalculate_portions_button_name,
        callback_data=f'{static_text.receipt_recalculate_portions_button_data}{receipt_id}'
    )

    edit_button = InlineKeyboardButton(
        static_text.receipt_edit_button_name,
        callback_data=f'{static_text.receipt_edit_button_data}{receipt_id}'
    )
    upload_photo = InlineKeyboardButton(
        static_text.receipt_photo_create_button_name,
        callback_data=f'{static_text.receipt_photo_create_button_data}{receipt_id}'
    )
    admnin_buttons = [edit_button, upload_photo]

    buttons = [
        [add_comment_button, recalculate_button],
    ]
    if comments_amount:
        buttons[0].append(comments_button)
    if user.is_telegram_admin:
        buttons.append(admnin_buttons)

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_category(category_id: int) -> InlineKeyboardMarkup:
    category_button = InlineKeyboardButton(
        static_text.category_view_button_name,
        callback_data=f'{static_text.category_view_button_data}{category_id}'
    )

    buttons = [
        [category_button],
    ]
    return InlineKeyboardMarkup(buttons)
