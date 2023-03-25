"""
    Telegram event handlers
"""
from telegram import Update
from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, CallbackContext, Updater
)

from receipt.settings import DEBUG
from telegram_bot.handlers.onboarding import handlers as onboarding_handlers
from telegram_bot.handlers.receipts import handlers as receipts_handlers
from telegram_bot.handlers.receipts import static_text as receipt_static_text
from telegram_bot.handlers.receipts.handlers import (
    upload_photo_conversation_handler,
    handle_upload_photo, new_portions_conversation_handler, handle_recalculating, handle_insert_portions,
)
from telegram_bot.main import bot
from telegram_bot.models import TelegramUser


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    dp.add_handler(CommandHandler("receipts", receipts_handlers.receipts))

    dp.add_handler(MessageHandler(Filters.text(receipt_static_text.list_receipt_text), receipts_handlers.receipts))
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.detail_receipt,
            pattern=rf'{receipt_static_text.receipt_view_button_data}\d+'
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.edit_receipt,
            pattern=rf'{receipt_static_text.receipt_edit_button_data}\d+'
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.view_comments,
            pattern=rf'{receipt_static_text.comments_list_button_data}\d+'
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.add_comment,
            pattern=rf'{receipt_static_text.comment_create_button_data}\d+'
        )
    )
    dp.add_handler(upload_photo_conversation_handler)
    dp.add_handler(
        CallbackQueryHandler(
            handle_upload_photo,
            pattern=rf'{receipt_static_text.receipt_photo_create_button_data}\d+'
        )
    )
    dp.add_handler(new_portions_conversation_handler)
    dp.add_handler(
        CallbackQueryHandler(
            handle_insert_portions,
            pattern=rf'{receipt_static_text.receipt_recalculate_portions_button_data}\d+'
        )
    )

    return dp


class CustomCallbackContext(CallbackContext):
    """Custom class for context."""

    def __init__(self, dispatcher: Dispatcher):
        super().__init__(dispatcher=dispatcher)
        self.user = None

    @staticmethod
    def get_user(update: Update):
        user_id = update.effective_user.id
        user_data = {
            'first_name': update.effective_message.from_user.first_name,
            'last_name': update.effective_message.from_user.last_name,
            'full_name': update.effective_message.from_user.full_name,
            'name': update.effective_message.from_user.name,
            'username': update.effective_message.from_user.username,
            'telegram_id': user_id,
        }
        user, _ = TelegramUser.objects.get_or_create(telegram_id=user_id, defaults=user_data)
        return user

    @classmethod
    def from_update(cls, update: object, dispatcher: Dispatcher) -> CallbackContext:
        context = super().from_update(update, dispatcher)
        if isinstance(update, Update) and update.effective_message:
            context.user = cls.get_user(update)
            return context


n_workers = 0 if DEBUG else 4
context_types = ContextTypes(context=CustomCallbackContext)
updater = Updater(bot=bot, context_types=context_types, workers=n_workers, use_context=True)

bot_dispatcher = setup_dispatcher(updater.dispatcher)
