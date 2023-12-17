from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_choose() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Choose category")
    return kb.as_markup(resize_keyboard=True)

def get_types_facts() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Get Science Fact')
    kb.button(text='Get History Fact')
    kb.button(text='Fact of the Day')
    kb.button(text='Exit')
    kb.adjust(4)

    return kb.as_markup(resize_keyboard=True)


def in_category_facts() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Send me fact')
    kb.button(text='Back')
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)

