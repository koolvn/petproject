import base64
import json
import logging
import time

import telebot
from kafka import KafkaProducer
from telebot.types import Message, CallbackQuery

from core.keyboards import *
from core.user import BotUser

time.sleep(15)  # Wait for other services to spin up
producer = KafkaProducer(bootstrap_servers='kafka:29092',
                         client_id='Test write',
                         buffer_memory=1e9,  # bytes
                         max_request_size=1e9,  # bytes
                         value_serializer=lambda v: json.dumps(v).encode('utf-8')
                         )


def bot_logic(bot: telebot.TeleBot):
    Vladimir = 208470137
    bot.send_message(Vladimir, 'Starting pet project...')
    default_params = {}

    # HANDLERS
    def reply_on_exception(message, exception):
        bot.send_message(chat_id=message.chat.id,
                         text='Кажется у нас проблемы 😢 Попробуй ещё раз позже',
                         reply_markup=custom_url_buttons({'Поддержка': 'https://t.me/kulyashov'}))
        bot.send_message(Vladimir,
                         f'There is a problem with this bot.\nException text: {exception}\n'
                         f'User: @{message.from_user.username} id:{message.from_user.id}\n'
                         f'Message: {message.text}'
                         )

    # Commands handlers
    @bot.message_handler(commands=['start'])
    def start_bot(message: Message):
        user = BotUser(link_source=message.text.split()[-1], **vars(message.from_user))
        if user.params:
            user.params.update(default_params)
        logging.info(f'/start from {user.__repr__()}\n{message.text}')
        bot.send_message(message.chat.id, f'\nПривет, {user.first_name}! '
                                          f'Задавай мне вопросы, а я буду отвечать!',
                         reply_markup=default_keyboard())
        bot.send_message(Vladimir, user.__repr__())

    @bot.message_handler(commands=['help'])
    def show_help(message: Message):
        logging.info(f'/help from id: {message.from_user.id}')
        bot.send_message(message.chat.id, f'Бот находится в разработке.\nБудет классно, если ты поможешь 😊',
                         reply_markup=help_keyboard(), disable_web_page_preview=True)

    # Message type handlers
    @bot.message_handler(func=lambda message: message.text != 'Настройки', content_types=['text'])
    def handle_text(message: Message):
        user = BotUser(**vars(message.from_user))
        logging.info(f'Received {message.content_type}'
                     f' from {message.from_user.first_name}'
                     f' @{message.from_user.username}'
                     f' ({message.from_user.id})')

        topic = 'tg_requests'
        data = {'user': int(user.id),
                'request': {'text': message.text,
                            'media': {}}
                }
        producer.send(topic, value=data, key=bytes(str(user.id), 'utf-8')).get(timeout=10)

    @bot.message_handler(content_types=['photo', 'document'])
    def handle_images(message: Message):
        logging.info(f'Received {message.content_type}'
                     f' from {message.from_user.first_name}'
                     f' @{message.from_user.username}'
                     f' ({message.from_user.id})')
        topic = 'tg_requests'
        bot.send_message(message.chat.id, f'Received {message.content_type}')
        bot.send_message(message.chat.id, "Ставлю в очередь...",
                         reply_markup=markup_keyboard())
        if message.content_type == 'photo':
            file_id = [x['file_id'] for x in message.json[message.content_type]][-1]
        else:
            file_id = message.json[message.content_type]['file_id']

        received_file_path = bot.get_file(file_id).file_path
        filename = received_file_path.split('/')[1]
        data_bytes = bot.download_file(received_file_path)
        data_bytes = base64.b64encode(data_bytes).decode('utf-8')
        data = {'user': f'{message.from_user.id}',
                'request': {'text': message.text,
                            'media': {'image_b64': data_bytes},
                            'filename': filename
                            },
                }
        result = producer.send(topic, value=data,
                               key=bytes(str(int(message.from_user.id)), 'utf-8')
                               ).get(timeout=10)

        bot.send_message(message.chat.id, f"Поставил\n{result = }", reply_markup=markup_keyboard())

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_handling(callback: CallbackQuery):
        user = BotUser(**vars(callback.from_user))
        logging.info(f'Callback from {user.__repr__()}:\n{callback.data}')
        if 'translate' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=True, text='Позже :)')
        if 'hello' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=False, text='Здравствуй!')
            # bot.send_voice(callback.from_user.id, open(PATH_TO_DATA + 'hello.ogg', 'rb'))

        elif 'help' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=False, text='')
            try:
                bot.edit_message_text(text=f'Бот находится в разработке.\nБудет классно, если ты поможешь 😊',
                                      chat_id=callback.message.chat.id,
                                      message_id=callback.message.message_id,
                                      reply_markup=help_keyboard())
            except Exception as e:
                logging.warning(str(e))
                show_help(callback.message)

        elif 'about' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=False, text='')
            # bot.send_voice(callback.from_user.id, open(PATH_TO_DATA + 'what_can_bot_do.ogg', 'rb'))
            # bot.send_video(callback.message.chat.id, open(PATH_TO_DATA + 'thanks.mp4', 'rb'))
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  text='Zaglushka',
                                  parse_mode='MarkdownV2',
                                  disable_web_page_preview=True,
                                  reply_markup=default_keyboard())

        elif 'settings' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=False, text='')
            try:
                bot.edit_message_text(text='Здесь будет можно поменять настройки',
                                      chat_id=callback.message.chat.id,
                                      message_id=callback.message.message_id,
                                      reply_markup=settings_keyboard(from_id=user.id),
                                      parse_mode='MarkdownV2')
            except Exception as e:
                logging.warning(str(e))
                bot.send_message(callback.message.chat.id,
                                 text='Здесь будет можно поменять настройки',
                                 reply_markup=settings_keyboard(from_id=user.id))

        elif 'back' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=False, text='')
            bot.edit_message_text('Рад стараться! Напиши мне или пришли голосовое сообщениe',
                                  chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  reply_markup=default_keyboard())

        elif 'choose_voice' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=False, text='')
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  text='zaglushka',
                                  reply_markup=voices_keyboard())

        elif 'choose_language' in callback.data:
            bot.answer_callback_query(callback_query_id=callback.id, show_alert=True,
                                      text='Пока не работает :(')


if __name__ == '__main__':
    print('This is a bot logic file. It can not be used separately!')
