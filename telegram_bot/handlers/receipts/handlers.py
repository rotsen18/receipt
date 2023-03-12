from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from culinary.api.v1.serializers.receipt import ReceiptListSerializer, ReceiptDetailSerializer
from culinary.models import Receipt
from telegram_bot.handlers.receipts import static_text
from telegram_bot.handlers.onboarding.keyboards import make_main_menu_keyboard
from telegram_bot.handlers.utils.info import extract_user_data_from_update
from telegram_bot.handlers.receipts import keyboards


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
        {'text': serializer.data.get('procedure'), 'reply_markup': make_main_menu_keyboard()},
    ]
    for message in messages:
        context.bot.send_message(
            user_id,
            parse_mode=ParseMode.HTML,
            **message
        )


def add_comment(update: Update, context: CallbackContext):
    pass