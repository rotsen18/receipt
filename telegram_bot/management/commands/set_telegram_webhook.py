import os

from django.core.management.base import BaseCommand
from telegram import Bot


class Command(BaseCommand):
    help = 'Sets Telegram webhooks'

    def handle(self, *args, **options):
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        webhook_endpoint = os.environ.get('TELEGRAM_WEBHOOK_ENDPOINT')
        if not bot_token or not webhook_endpoint:
            self.stdout.write(self.style.ERROR('Please set TELEGRAM_BOT_TOKEN and TELEGRAM_WEBHOOK_ENDPOINT in your .env file'))
            return
        webhook_url = f'https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_endpoint}'
        bot = Bot(token=bot_token)
        result = bot.setWebhook(url=webhook_url)

        if result:
            self.stdout.write(self.style.SUCCESS('Webhook set successfully'))
        else:
            self.stdout.write(self.style.ERROR('Failed to set webhook'))
