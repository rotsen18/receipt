from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from culinary.api.v1.serializers.receipt import ReceiptListSerializer, ReceiptDetailSerializer
from culinary.models import Receipt
from telegram_bot.handlers.receipts import static_text
from telegram_bot.handlers.receipts.keyboards import make_menu_keyboard
from telegram_bot.handlers.utils.info import extract_user_data_from_update
from telegram_bot.models import TelegramUser
from telegram_bot.handlers.receipts import keyboards


def command_start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = {
        'first_name': update.message.from_user.first_name,
        'last_name': update.message.from_user.last_name,
        'username': update.message.from_user.username,
        'telegram_id': user_id,
    }
    u, created = TelegramUser.objects.get_or_create(telegram_id=user_id, defaults=user_data)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text, reply_markup=keyboards.make_keyboard_for_start_command())


def receipts(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    receipts = Receipt.objects.all()
    serializer = ReceiptListSerializer(instance=receipts, many=True)
    for data in serializer.data:
        text = static_text.receipt_short_text.format(**data)
        context.bot.send_message(
            user_id,
            text,
            reply_markup=keyboards.make_keyboard_for_receipt(receipt_id=1),
            parse_mode=ParseMode.HTML
        )


def detail_receipt(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    receipt_id = int(update.callback_query.data.replace('receipt_id=', ''))
    serializer = ReceiptDetailSerializer(Receipt.objects.get(id=receipt_id))
    messages = [
        {'text': static_text.receipt_detail_title.format(**serializer.data)},
        {'text': '\n'.join([f'{num}. {value}' for num, value in enumerate(serializer.data.get('components'), 1)])},
        {'text': serializer.data.get('procedure'), 'reply_markup': make_menu_keyboard()},
    ]
    for message in messages:
        context.bot.send_message(
            user_id,
            parse_mode=ParseMode.HTML,
            **message
        )
