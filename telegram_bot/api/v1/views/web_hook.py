from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from telegram import Update

from telegram_bot.dispatcher import bot_dispatcher
from telegram_bot.main import bot

# 'https://api.telegram.org/bot{token}?url={domain}/api/v1/telegram_bot/webhook'


class WebHookView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        update = Update.de_json(data, bot)
        bot_dispatcher.process_update(update)
        return Response('ok')

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({'ok': 'Get request received! But nothing done'})
