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
from telegram_bot.handlers.onboarding.static_text import list_receipt_text
from telegram_bot.main import bot


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    dp.add_handler(CommandHandler("receipts", onboarding_handlers.receipts))
    dp.add_handler(MessageHandler(Filters.text(list_receipt_text), onboarding_handlers.receipts))
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.detail_receipt, pattern=f"receipt_id=\d+"))

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
