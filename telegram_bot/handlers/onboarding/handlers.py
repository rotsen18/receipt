from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.handlers.onboarding import static_text
from telegram_bot.models import TelegramUser
from telegram_bot.handlers.onboarding import keyboards


def command_start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = {
        'first_name': update.message.from_user.first_name,
        'last_name': update.message.from_user.last_name,
        'username': update.message.from_user.username,
        'telegram_id': user_id,
    }
    user, created = TelegramUser.objects.get_or_create(telegram_id=user_id, defaults=user_data)

    if created:
        text = static_text.start_created.format(first_name=user.first_name)
    else:
        text = static_text.start_not_created.format(first_name=user.first_name)

    update.message.reply_text(text=text, reply_markup=keyboards.make_keyboard_for_start_command(user))
