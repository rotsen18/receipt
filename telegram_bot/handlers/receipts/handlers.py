from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from culinary.api.v1.serializers.receipt import ReceiptListSerializer, ReceiptDetailSerializer
from culinary.models import Receipt, ReceiptComment
from telegram_bot.handlers.handlers import not_implemented
from telegram_bot.handlers.receipts import static_text
from telegram_bot.handlers.receipts.serializers import BotReceiptCommentSerializer
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
    receipt_id = int(update.callback_query.data.replace(static_text.receipt_view_button_data, ''))
    receipt = Receipt.objects.get(id=receipt_id)
    serializer = ReceiptDetailSerializer(receipt)
    messages = [
        {'text': static_text.receipt_detail_title.format(**serializer.data)},
        {'text': '\n'.join([f'{num}. {value}' for num, value in enumerate(serializer.data.get('components'), 1)])},
        {
            'text': serializer.data.get('procedure'),
            'reply_markup': keyboards.make_keyboard_for_detail_receipt(receipt_id, receipt.comments.count())
        },
    ]
    for message in messages:
        context.bot.send_message(
            user_id,
            parse_mode=ParseMode.HTML,
            **message
        )


@not_implemented
def edit_receipt(update: Update, context: CallbackContext):
    pass


def view_comments(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    receipt_id = int(update.callback_query.data.replace(static_text.comments_list_button_data, ''))
    comments = ReceiptComment.objects.filter(receipt_id=receipt_id)
    serializer = BotReceiptCommentSerializer(instance=comments, many=True)
    for comment in serializer.data:
        context.bot.send_message(
            user_id,
            parse_mode=ParseMode.HTML,
            text=static_text.comment_view.format(**comment)
        )


@not_implemented
def add_comment(update: Update, context: CallbackContext):
    pass
