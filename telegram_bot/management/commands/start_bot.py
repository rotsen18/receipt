from django.core.management.base import BaseCommand

from telegram_bot.run_polling import run_polling


class Command(BaseCommand):
    help = 'Sets Telegram webhooks'

    def handle(self, *args, **options):
        run_polling()
        return
