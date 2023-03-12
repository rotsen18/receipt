from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from culinary.api.v1.serializers.receipt import ReceiptListSerializer, ReceiptDetailSerializer
from culinary.models import Receipt
from telegram_bot.handlers.receipts import static_text
from telegram_bot.handlers.utils.info import extract_user_data_from_update
from telegram_bot.models import TelegramUser
from telegram_bot.handlers.receipts import keyboards


def new_receipt(update: Update, context: CallbackContext):
    pass


def new_component(update: Update, context: CallbackContext):
    pass


def new_cooking_principe(update: Update, context: CallbackContext):
    pass


def new_category(update: Update, context: CallbackContext):
    pass


def new_component(update: Update, context: CallbackContext):
    pass
