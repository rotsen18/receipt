from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import Count
from django.urls import reverse
from telegram import ChatAction, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

from culinary.api.v1.serializers.receipt import ReceiptListSerializer
from culinary.models import Receipt, ReceiptComment, ReceiptSource
from culinary.services import PortionService, ReceiptPriceService
from directory.models import CulinaryCategory
from telegram_bot.handlers.handlers import not_implemented
from telegram_bot.handlers.receipts import keyboards, static_text
from telegram_bot.handlers.receipts.serializers import (
    BotCulinaryCategorySerializer, BotDetailReceiptSerializer, BotReceiptCommentSerializer, ReceiptSourceSerializer,
)
from telegram_bot.handlers.utils.info import extract_user_data_from_update
from telegram_bot.main import bot

UPLOAD_PHOTO = range(1)
RECALCULATE_PORTIONS = range(1)
STORE_SOURCE = range(1)
VOTE_RECEIPT, ADD_COMMENT = range(2)


def receipts(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    receipts = Receipt.objects.all()
    serializer = ReceiptListSerializer(instance=receipts, many=True)
    for data in serializer.data:
        text = static_text.receipt_short_text.format(**data)
        keyboard = keyboards.make_keyboard_for_receipt(
            user=context.user,
            receipt_id=data.get('id'),
            category_name=data.get('category_name'),
            category_id=data.get('category_id'),
        )
        context.bot.send_message(
            user_id,
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )


def get_components(data):
    parts = []
    for header, components in data.get('components').items():
        components_list_text = '\n'.join([f'{num}. {value}' for num, value in enumerate(components, 1)])
        part = f'{header.capitalize()}:\n{components_list_text}'
        parts.append(part)
    return '\n\n'.join(parts)


def detail_receipt(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    receipt_id = int(update.callback_query.data.replace(static_text.receipt_view_button_data, ''))
    receipt = Receipt.objects.get(id=receipt_id)
    serializer = BotDetailReceiptSerializer(receipt)
    data = serializer.data
    data['devices'] = ', '.join(data.get('devices'))
    messages = [
        {'text': static_text.receipt_detail_title.format(**data)},
        {'text': get_components(serializer.data)},
        {
            'text': serializer.data.get('procedure'),
            'reply_markup': keyboards.make_keyboard_for_detail_receipt(
                user=context.user,
                receipt_id=receipt_id,
                comments_amount=receipt.comments.count(),
            ),
        },
    ]
    if receipt.photo:
        try:
            context.bot.send_photo(user_id, receipt.photo)
        except FileNotFoundError:
            pass  # photo was stored on production server
    for message in messages:
        context.bot.send_message(
            user_id,
            parse_mode=ParseMode.HTML,
            **message
        )


@not_implemented
def edit_receipt(update: Update, context: CallbackContext):
    pass


def add_receipt(update: Update, context: CallbackContext):
    create_url = reverse('admin:culinary_receipt_add')
    base_url = settings.RENDER_EXTERNAL_HOSTNAME
    update.message.reply_text(text=f'{base_url}{create_url}')


def view_comments(update: Update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    receipt_id = int(update.callback_query.data.replace(static_text.comments_list_button_data, ''))
    comments = ReceiptComment.objects.filter(receipt_id=receipt_id)
    serializer = BotReceiptCommentSerializer(instance=comments, many=True)
    for comment in serializer.data:
        context.bot.send_message(
            user_id,
            parse_mode=ParseMode.HTML,
            text=static_text.comment_view.format(**comment),
        )


@not_implemented
def add_comment(update: Update, context: CallbackContext):
    pass


def handle_upload_photo(update, context):
    receipt_id = int(update.callback_query.data.replace(static_text.receipt_photo_create_button_data, ''))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please upload a photo for your receipt.')
    context.user_data['upload_photo'] = True
    context.chat_data['receipt_id'] = receipt_id
    return UPLOAD_PHOTO


def handle_photo(update, context: CallbackContext):
    receipt_id = context.chat_data.get('receipt_id')
    receipt = Receipt.objects.get(id=receipt_id)
    photo = update.message.photo[-1]  # Get the largest available photo
    file_id = photo.file_id
    name = photo.file_unique_id
    file = bot.get_file(file_id)
    file_bytes = file.download_as_bytearray()
    receipt.photo.save(name, ContentFile(file_bytes))
    context.bot.send_message(chat_id=update.effective_chat.id, text='The photo has been uploaded.')
    context.user_data.clear()
    return ConversationHandler.END


upload_photo_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(handle_upload_photo, pattern=rf'{static_text.receipt_photo_create_button_data}\d+'),
    ],
    states={
        UPLOAD_PHOTO: [MessageHandler(Filters.photo, handle_photo)],
    },
    fallbacks=[],
)


def handle_insert_portions(update, context: CallbackContext):
    receipt_id = int(update.callback_query.data.replace(static_text.receipt_recalculate_portions_button_data, ''))
    receipt = Receipt.objects.get(id=receipt_id)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=static_text.recalculate_portion_question.format(previous_portions=receipt.receipt_portions)
    )
    context.chat_data['receipt_id'] = receipt_id
    return RECALCULATE_PORTIONS


def handle_recalculating(update, context: CallbackContext):
    receipt_id = context.chat_data.get('receipt_id')
    receipt = Receipt.objects.get(id=receipt_id)
    portions = int(update.message.text)
    new_data = PortionService.new_portions(receipt=receipt, portions=portions)
    title = static_text.recalculate_result_title.format(new_portions=portions)
    answer = [title]
    for num, component in enumerate(new_data, 1):
        row = f"{num}. {component.get('ingredient_name')} " \
              f"- {component.get('new_amount')} {component.get('measurement_unit_name')}"
        answer.append(row)

    text = '\n'.join(answer)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return ConversationHandler.END


new_portions_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            handle_insert_portions,
            pattern=rf'{static_text.receipt_recalculate_portions_button_data}\d+',
        ),
    ],
    states={
        RECALCULATE_PORTIONS: [
            MessageHandler(Filters.text, handle_recalculating),
        ],
    },
    fallbacks=[],
)


def handle_all_categories(update, context: CallbackContext):
    categories = CulinaryCategory.objects.annotate(receipt_count=Count('receipt'))
    serializer = BotCulinaryCategorySerializer(instance=categories, many=True)
    text = static_text.category__list_view_result_text
    keyboard = keyboards.make_keyboard_for_category(serializer.data)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def handle_category(update, context: CallbackContext):
    user_id = extract_user_data_from_update(update)['user_id']
    category_id = int(update.callback_query.data.replace(static_text.category_view_button_data, ''))
    receipts = Receipt.objects.filter(category_id=category_id)
    serializer = ReceiptListSerializer(instance=receipts, many=True)
    for data in serializer.data:
        text = static_text.receipt_short_text_with_description.format(**data)
        keyboard = keyboards.make_keyboard_for_receipt(
            user=context.user,
            receipt_id=data.get('id'),
            category_name=data.get('category_name'),
            category_id=data.get('category_id'),
        )
        context.bot.send_message(
            user_id,
            text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )


def unknown_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=static_text.unknown_command)


def handle_insert_source(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=static_text.receipt_source_question_text)
    return STORE_SOURCE


def handle_source(update, context: CallbackContext):
    ReceiptSource.objects.get_or_create(source=update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=static_text.receipt_source_saved_text)
    return ConversationHandler.END


new_receipt_source_conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex(static_text.receipt_source_create_button_name),
            handle_insert_source,
        ),
    ],
    states={
        STORE_SOURCE: [
            MessageHandler(Filters.text, handle_source),
        ],
    },
    fallbacks=[],
)


def handle_sources(update, context: CallbackContext):
    sources = ReceiptSource.objects.all()
    serializer = ReceiptSourceSerializer(instance=sources, many=True)
    for source in serializer.data:
        text = static_text.receipt_source_item_text.format(**source)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


def handle_ask_vote(update, context: CallbackContext):
    receipt_id = int(update.callback_query.data.replace(static_text.comment_create_button_data, ''))
    keyboard = keyboards.make_keyboard_for_receipt_vote()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=static_text.comment_vote_text,
        reply_markup=keyboard,
    )
    context.chat_data['receipt_id'] = receipt_id
    return VOTE_RECEIPT


def handle_vote(update, context: CallbackContext):
    receipt_id = context.chat_data.get('receipt_id')
    vote = int(update.callback_query.data.replace(static_text.comment_vote_button_data, ''))
    comment = ReceiptComment.objects.create(telegram_user=context.user, receipt_id=receipt_id, rate=vote)
    context.chat_data['comment_id'] = comment.id

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=static_text.comment_vote_accepted_text,
    )
    return ADD_COMMENT


def handle_add_comment(update, context: CallbackContext):
    comment_id = context.chat_data.get('comment_id')
    comment = ReceiptComment.objects.get(id=comment_id)
    comment.text = update.message.text
    comment.save(update_fields=['text'])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=static_text.comment_added_text,
    )
    return ConversationHandler.END


add_comment_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            handle_ask_vote,
            pattern=rf'{static_text.comment_create_button_data}\d+'
        )
    ],
    states={
        VOTE_RECEIPT: [
            CallbackQueryHandler(
                handle_vote,
                pattern=rf'{static_text.comment_vote_button_data}\d+',
            )
        ],
        ADD_COMMENT: [
            MessageHandler(Filters.text, handle_add_comment),
        ],
    },
    fallbacks=[],
)


def handle_receipt_price(update, context: CallbackContext):
    receipt_id = int(update.callback_query.data.replace(static_text.receipt_price_view_button_data, ''))
    receipt = Receipt.objects.get(id=receipt_id)
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    price_calculator = ReceiptPriceService(receipt)
    ingredients_price_text = '\n'.join(price_calculator.get_components_price_text())
    receipt_cost = round(price_calculator.products_cost + price_calculator.consumption_cost, 2)
    receipt_cost_per_portion = round(receipt_cost / receipt.receipt_portions, 2)
    one_pcs_price = round(price_calculator.receipt_price / receipt.receipt_portions, 2)
    text = static_text.receipt_price_view_text.format(
        products_cost=price_calculator.products_cost,
        ingredients_price=ingredients_price_text,
        consumption_cost=price_calculator.consumption_cost,
        receipt_cost=receipt_cost,
        profit_percent=settings.PROFIT_PERCENT * 100,
        profit_cost=price_calculator.profit_cost,
        total_price=price_calculator.receipt_price,
        receipt_cost_per_portion=receipt_cost_per_portion,
        one_pcs_price=one_pcs_price,
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
