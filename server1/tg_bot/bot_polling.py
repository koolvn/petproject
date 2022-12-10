import sys

import telebot
import logging
from _secret import bot_token
from bot_logic import bot_logic

LOG_LEVEL = logging.INFO
if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    bot = telebot.TeleBot(bot_token)
    bot_logic(bot)
    bot.polling(none_stop=True, interval=1)
