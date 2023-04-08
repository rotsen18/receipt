import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receipt.settings')
django.setup()

from telegram import Bot, BotCommand  # noqa E402
from telegram.ext import Updater  # noqa E402

from receipt.settings import DEBUG, TELEGRAM_BOT_TOKEN  # noqa E402
from telegram_bot.dispatcher import context_types  # noqa E402
from telegram_bot.dispatcher import setup_dispatcher  # noqa E402


def run_polling(tg_token: str = TELEGRAM_BOT_TOKEN):
    """ Run bot in polling mode """
    n_workers = 0 if DEBUG else 4

    updater = Updater(token=tg_token, context_types=context_types, workers=n_workers, use_context=True)
    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot = Bot(tg_token)
    bot_info = bot.get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)
    bot.delete_webhook()
    bot.delete_my_commands()
    bot.set_my_commands(
        commands=[
            BotCommand('start', 'Почати 🚀'), BotCommand('receipts', 'Показати всі рецептиs 📊'),
        ],
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_polling()
