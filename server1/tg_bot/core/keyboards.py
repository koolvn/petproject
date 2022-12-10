# Keyboards
__all__ = ['default_keyboard', 'settings_keyboard', 'custom_url_buttons',
           'help_keyboard', 'voices_keyboard', 'markup_keyboard', 'remove_keyboard']

from telebot.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


def default_keyboard():
    keyboard = InlineKeyboardMarkup()
    # ssml = InlineKeyboardButton(text='Что такое SSML?',
    #                             url='https://cloud.yandex.ru/docs/speechkit/tts/ssml')
    about = InlineKeyboardButton('Расскажи, что умеешь', callback_data='about')
    settings = InlineKeyboardButton('Настройки', callback_data='settings')
    helpme = InlineKeyboardButton('Помощь', callback_data='help')
    keyboard.row_width = 2
    keyboard.add(about, settings, helpme)
    return keyboard


def settings_keyboard(**kwargs):
    keyboard = InlineKeyboardMarkup()
    # keyboard.add(InlineKeyboardButton('Выбрать голос', callback_data='choose_voice'))
    # keyboard.add(InlineKeyboardButton('Выбрать язык', callback_data='choose_language'))
    keyboard.row(InlineKeyboardButton('🔙 назад', callback_data='back'))
    return keyboard


def voices_keyboard():
    keyboard = InlineKeyboardMarkup()
    # keyboard.row(*[InlineKeyboardButton(name,
    #                                     callback_data=f'{name}') for name in
    #                ['Филипп', 'Захар', 'Эрмиль']])
    # keyboard.row(*[InlineKeyboardButton(name,
    #                                     callback_data=f'{name}') for name in
    #                ['Оксана', 'Женя', 'Алёна', 'Омаж']])
    keyboard.row(InlineKeyboardButton('🔙 назад', callback_data='back_to_settings'))
    return keyboard


def custom_url_buttons(btn_names: dict):
    keyboard = InlineKeyboardMarkup()
    for cb_data, btn in btn_names.items():
        keyboard.add(InlineKeyboardButton(cb_data, callback_data=cb_data, url=btn))
    return keyboard


def help_keyboard():
    # {'Доступные голоса': 'https://cloud.yandex.ru/docs/speechkit/tts/#voices',
    #  'Описание методов': 'https://cloud.yandex.ru/docs/speechkit/tts/request',
    #  'Хочу помочь!': 'https://money.yandex.ru/to/410014485115217',
    #  'Ответы на вопросы': 'https://t.me/kulyashov'}
    keyboard = custom_url_buttons({})
    keyboard.add(InlineKeyboardButton('🔙 назад', callback_data='back'))
    return keyboard


def markup_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=False)
    keyboard.row('/start', '/help')
    keyboard.row('Настройки')
    # keyboard.row('Скрыть')
    return keyboard


def remove_keyboard():
    keyboard = ReplyKeyboardRemove()
    return keyboard


def translate_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('Перевести', callback_data='translate'))
    return keyboard
