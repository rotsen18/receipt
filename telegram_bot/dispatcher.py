"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from receipt.settings import DEBUG
from telegram_bot.handlers.onboarding import handlers as onboarding_handlers
from telegram_bot.handlers.receipts import handlers as receipts_handlers
from telegram_bot.handlers.receipts import static_text as receipt_static_text
from telegram_bot.main import bot


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    dp.add_handler(CommandHandler("receipts", receipts_handlers.receipts))

    dp.add_handler(MessageHandler(Filters.text(receipt_static_text.list_receipt_text), receipts_handlers.receipts))
    dp.add_handler(CallbackQueryHandler(
        receipts_handlers.detail_receipt,
        pattern=rf'{receipt_static_text.receipt_view_button_data}\d+')
    )
    dp.add_handler(CallbackQueryHandler(
        receipts_handlers.edit_receipt,
        pattern=rf'{receipt_static_text.receipt_edit_button_data}\d+')
    )
    dp.add_handler(CallbackQueryHandler(
        receipts_handlers.view_comments,
        pattern=rf'{receipt_static_text.comments_list_button_data}\d+')
    )
    dp.add_handler(CallbackQueryHandler(
            receipts_handlers.add_comment,
            pattern=rf'{receipt_static_text.comment_create_button_data}\d+'
        )
    )
    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
