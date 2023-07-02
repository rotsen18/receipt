from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from culinary.api.v1.serializers.receipt import ReceiptListSerializer
from culinary.models import Receipt
from telegram_bot.handlers.onboarding import keyboards, static_text
from telegram_bot.models import TelegramUser


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


def command_catalogue(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    for receipt in Receipt.objects.all():
        data = ReceiptListSerializer(receipt).data
        text = static_text.catalogue_item_title.format(**data)
        if receipt.photo:
            try:
                context.bot.send_photo(user_id, receipt.photo, caption=text, parse_mode=ParseMode.HTML)
            except FileNotFoundError:
                pass
        else:
            context.bot.send_message(user_id, parse_mode=ParseMode.HTML, text=text)
