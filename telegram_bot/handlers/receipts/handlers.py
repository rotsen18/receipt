from django.db.models import Count
from telegram import ParseMode, Update
from telegram.ext import (
    CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters,
)

from culinary.api.v1.serializers.receipt import ReceiptListSerializer, ReceiptDetailSerializer
from culinary.models import Receipt, ReceiptComment, ReceiptImage
from culinary.services import PortionService
from directory.models import CulinaryCategory
from telegram_bot.handlers.handlers import not_implemented
from telegram_bot.handlers.receipts import static_text
from telegram_bot.handlers.receipts.serializers import BotReceiptCommentSerializer, BotCulinaryCategorySerializer
from telegram_bot.handlers.utils.info import extract_user_data_from_update
from telegram_bot.handlers.receipts import keyboards

UPLOAD_PHOTO = range(1)
RECALCULATE_PORTIONS = range(1)


def receipts(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    receipts = Receipt.objects.all()
    serializer = ReceiptListSerializer(instance=receipts, many=True)
    for data in serializer.data:
        text = static_text.receipt_short_text.format(**data)
        keyboard = keyboards.make_keyboard_for_receipt(
            receipt_id=data.get('id'),
            category_name=data.get('category_name'),
            category_id=data.get('category_id')
        )
        context.bot.send_message(
            user_id,
            text,
            reply_markup=keyboard,
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
            'reply_markup': keyboards.make_keyboard_for_detail_receipt(
                user=context.user,
                receipt_id=receipt_id,
                comments_amount=receipt.comments.count()
            )
        },
    ]
    for image in receipt.photos.all():
        context.bot.send_photo(user_id, image.photosize)
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


def handle_upload_photo(update, context):
    receipt_id = int(update.callback_query.data.replace(static_text.receipt_photo_create_button_data, ''))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload a photo for your receipt.")
    context.user_data['upload_photo'] = True
    context.chat_data['receipt_id'] = receipt_id
    return UPLOAD_PHOTO


def handle_photo(update, context):
    receipt_id = context.chat_data.get('receipt_id')

    ReceiptImage.objects.get_or_create(
        receipt_id=receipt_id,
        file_id=update.message.photo[-1].file_id,
        file_size=update.message.photo[-1].file_size,
        file_unique_id=update.message.photo[-1].file_unique_id,
        height=update.message.photo[-1].height,
        width=update.message.photo[-1].width
    )

    context.bot.send_message(chat_id=update.effective_chat.id, text="The photo has been uploaded.")
    context.user_data.clear()
    return ConversationHandler.END


upload_photo_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(handle_upload_photo, pattern=rf'{static_text.receipt_photo_create_button_data}\d+')
    ],
    states={
        UPLOAD_PHOTO: [MessageHandler(Filters.photo, handle_photo)],
    },
    fallbacks=[],
)


def handle_insert_portions(update, context):
    receipt_id = int(update.callback_query.data.replace(static_text.receipt_recalculate_portions_button_data, ''))
    context.bot.send_message(chat_id=update.effective_chat.id, text=static_text.recalculate_portion_question)
    context.chat_data['receipt_id'] = receipt_id
    return RECALCULATE_PORTIONS


def handle_recalculating(update, context):
    receipt_id = context.chat_data.get('receipt_id')
    receipt = Receipt.objects.get(id=receipt_id)
    portions = int(update.message.text)

    new_data = PortionService.new_portions(receipt=receipt, portions=portions)
    title = static_text.recalculate_result_title.format(
        previous_portions=receipt.receipt_portions,
        new_portions=portions
    )

    answer = [title]
    for num, component in enumerate(new_data, 1):
        row = f"{num}. {component.get('name')} - {component.get('amount')} {component.get('measurement_unit')}"
        answer.append(row)

    text = '\n'.join(answer)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return ConversationHandler.END


new_portions_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            handle_insert_portions,
            pattern=rf'{static_text.receipt_recalculate_portions_button_data}\d+'
        )
    ],
    states={
        RECALCULATE_PORTIONS: [
            MessageHandler(Filters.text, handle_recalculating)
        ]
    },
    fallbacks=[],
)


def handle_all_categories(update, context):
    categories = CulinaryCategory.objects.annotate(receipt_count=Count('receipt'))
    serializer = BotCulinaryCategorySerializer(instance=categories, many=True)

    for category in serializer.data:
        text = static_text.category_description.format(
            name=category.get('name'),
            receipt_count=category.get('receipt_count'),
            description=category.get('description'),
        )
        keyboard = None
        if category.get('receipt_count'):
            keyboard = keyboards.make_keyboard_for_category(category_id=category.get('id'))
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )


def handle_category(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    category_id = int(update.callback_query.data.replace(static_text.category_view_button_data, ''))
    receipts = Receipt.objects.filter(category_id=category_id)
    serializer = ReceiptListSerializer(instance=receipts, many=True)
    for data in serializer.data:
        text = static_text.receipt_short_text.format(**data)
        keyboard = keyboards.make_keyboard_for_receipt(
            receipt_id=data.get('id'),
            category_name=data.get('category_name'),
            category_id=data.get('category_id')
        )
        context.bot.send_message(
            user_id,
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
