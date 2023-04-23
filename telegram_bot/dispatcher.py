from telegram import Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler, CommandHandler, ContextTypes, Dispatcher, Filters, MessageHandler, Updater,
)

from receipt.settings import DEBUG
from telegram_bot.handlers.onboarding import handlers as onboarding_handlers
from telegram_bot.handlers.onboarding import static_text as onboarding_static_text
from telegram_bot.handlers.receipts import handlers as receipts_handlers
from telegram_bot.handlers.receipts import static_text as receipt_static_text
from telegram_bot.main import bot
from telegram_bot.models import TelegramUser


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', onboarding_handlers.command_start))
    dp.add_handler(CommandHandler('receipts', receipts_handlers.receipts))

    dp.add_handler(MessageHandler(Filters.text(receipt_static_text.list_receipt_text), receipts_handlers.receipts))
    dp.add_handler(
        MessageHandler(
            Filters.text(onboarding_static_text.list_categories),
            receipts_handlers.handle_all_categories
        )
    )
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
    dp.add_handler(receipts_handlers.upload_photo_conversation_handler)
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.handle_upload_photo,
            pattern=rf'{receipt_static_text.receipt_photo_create_button_data}\d+'
        )
    )
    dp.add_handler(receipts_handlers.new_portions_conversation_handler)
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.handle_insert_portions,
            pattern=rf'{receipt_static_text.receipt_recalculate_portions_button_data}\d+'
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.handle_category,
            pattern=rf'{receipt_static_text.category_view_button_data}\d+'
        )
    )
    dp.add_handler(
        MessageHandler(
            Filters.text(receipt_static_text.receipt_create_button_name),
            receipts_handlers.add_receipt
        )
    )
    dp.add_handler(receipts_handlers.new_receipt_source_conversation_handler)
    dp.add_handler(
        MessageHandler(
            Filters.regex(receipt_static_text.receipt_source_create_button_name),
            receipts_handlers.handle_insert_source,
        ),
    )
    dp.add_handler(
        MessageHandler(
            Filters.text(receipt_static_text.receipt_source_list_button_name),
            receipts_handlers.handle_sources
        )
    )
    dp.add_handler(receipts_handlers.add_comment_conversation_handler)
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.handle_ask_vote,
            pattern=rf'{receipt_static_text.comment_create_button_data}\d+'
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            receipts_handlers.handle_receipt_price,
            pattern=rf'{receipt_static_text.receipt_price_view_button_data}\d+'
        )
    )
    # unknown command
    dp.add_handler(
        MessageHandler(Filters.text, receipts_handlers.unknown_command)
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
