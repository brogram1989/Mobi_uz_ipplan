from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class InlineKeyboardBuilder:
    def __init__(self):
        self.keyboard = []

    def add_button(self, text, callback_data):
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        self.keyboard.append([button])

    def create_keyboard(self):
        return InlineKeyboardMarkup(inline_keyboard=self.keyboard)
