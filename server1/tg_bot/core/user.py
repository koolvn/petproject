__all__ = ['BotUser']

from telebot.types import User


class BotUser(User):
    def __init__(self, id, is_bot, first_name, **kwargs):
        super().__init__(id, is_bot, first_name)
        self.params = None
        self.start_dt = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'BotUser: @{self.username}, name: {self.first_name}, id:{self.id}'

    def __getitem__(self, item):
        return getattr(self, item)
