from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

MAC_adress = ['1223:1441:3451:3161','1231:1426:3436:3621','1122:1264:3364:3161','1622:1724:3824:3211']


def inl_kb_builder():
    builder = ReplyKeyboardBuilder()
    for item in [str(i) for i in MAC_adress]:
        builder.button(text=f'{item}')
    builder.button(text='Назад')
    builder.adjust(1) 
    return builder.as_markup(resize_keyboard = True)
    

# main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Устройства')],
#                                      [KeyboardButton(text='Добавить адрес')]], 
#                                       resize_keyboard=True,
#                                       input_field_placeholder='Выберите пункт меню...',
#                                       one_time_keyboard=True)


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Подключиться')],
                                     [KeyboardButton(text='Отключиться')]], 
                                      resize_keyboard=True,
                                      input_field_placeholder='Выберите пункт меню...',
                                      one_time_keyboard=True)


MAC = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Подключиться', callback_data = 'Connection')],
                                            [InlineKeyboardButton(text='Отключиться', callback_data = 'Disconnection')]])


# main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Устройства', callback_data='units')],
#                                                 [InlineKeyboardButton(text='Добавить адрес', callback_data='add_address')],
#                                                 [InlineKeyboardButton(text='123', callback_data='123')]])