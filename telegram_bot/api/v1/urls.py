from django.urls import path

from telegram_bot.api.v1.views.web_hook import WebHookView

urlpatterns = [
    path('webhook/', WebHookView.as_view())
]
