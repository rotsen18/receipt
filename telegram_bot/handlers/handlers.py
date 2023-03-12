from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.handlers.onboarding import static_text
from telegram_bot.handlers.utils.info import extract_user_data_from_update


def not_implemented(func):
    def decorator(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = extract_user_data_from_update(update)['user_id']
        context.bot.send_message(user_id, text=static_text.not_implemented)
        return func(update, context, *args, **kwargs)

    return decorator
