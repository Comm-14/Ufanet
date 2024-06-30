import re
from aiogram import F, Router, types, Bot
from aiogram.types import Message, CallbackQuery, BotCommand, BotCommandScopeDefault
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
import redis
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiomqtt_sub import listen
import asyncio

from bot_test.keyboard import inl_kb_builder

import bot_test.keyboard as kb  

router = Router()

User_id = [] # Список с айдишниками юзера

MAC_adress = ['1223:1441:3451:3161','1231:1426:3436:3621','1122:1264:3364:3161','1622:1724:3824:3211']
redis_bd = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True # <-- this will ensure that binary data is decoded
)


class state_adr(StatesGroup):
    chosing_adr = State()
    disconnect = State()

async def set_commands():
    commands = [BotCommand(command='start',),
                BotCommand(command='id',)]
    await Bot.set_my_commands(commands,BotCommandScopeDefault())

# async def run_sub(topic):
#     task = asyncio.create_task(main(topic))
#     await task()


@router.message(CommandStart())
async def cmd_start(message: Message):
    # User_id.append(message.from_user.id)  #Сохранение User_id пользователя при отправке команды /start
    # print(User_id)
    await message.answer("Привет!", reply_markup = kb.main)


@router.message(StateFilter(None), F.text == 'Подключиться')
async def mac_input(message: Message, state: FSMContext):
    await message.answer('Введите MAC-адрес:')
    await state.set_state(state_adr.chosing_adr)
    

@router.message(state_adr.chosing_adr)
async def mac_input(message: Message, state: FSMContext):
    mac = message.text
    if re.match(r'\d{4}:\d{4}:\d{4}:\d{4}', mac):
        idd = str(message.from_user.id)  #Сохранение User_id пользователя при успешном подключении
        if redis_bd.sadd(mac, idd):
            await message.answer(f'Вы подключены к адресу: {mac}')
            await state.clear()
            try:
                async with asyncio.timeout(60):
                    while True:
                        if redis_bd.sismember(mac, idd):
                            await message.answer(f'Message from {mac}:\n{await listen(mac)}')
                        else:
                            break
                        
            except asyncio.TimeoutError:
                print(f"timeout {mac}, id: {idd}")
                redis_bd.srem(mac, idd)
                await message.answer(f'Вы отключены от адреса: {mac}')
        else:
            await message.answer('Вы уже подключену к данному MAC')
    else: 
        await message.answer('Вы ввели неверный MAC-адрес, попробуйте еще раз', reply_markup=kb.main)
    


#--------------------------------------------------------------------------------------
    

@router.message(StateFilter(None), F.text == 'Отключиться')
async def output(message: Message, state: FSMContext):
    await message.answer('Введите MAC-адрес от которого хотите отписаться:')
    await state.set_state(state_adr.disconnect)


@router.message(state_adr.disconnect)
async def mac_output(message: Message, state: FSMContext):
    mac = message.text
    if re.match(r'\d{4}:\d{4}:\d{4}:\d{4}', mac):
        idd = str(message.from_user.id)  #Сохранение User_id пользователя при успешном подключении
        if redis_bd.srem(mac, idd):
            await message.answer(f'Вы отключены от адреса: {mac}')
            await state.clear()
        else:
            await message.answer(f'Вы не подписаны на MAC: {mac}')
    else: 
        await message.answer('Вы ввели неверный MAC-адрес', reply_markup=kb.main)
        


# @router.message(F.text == "Устройства")
# async def reply_builder(message: Message):
#     await message.answer(
#         "Выберите устройство:",
#         reply_markup=inl_kb_builder()
#     )



#-------------------------------------------------------------------------------

@router.message(Command('id'))
async def alarm(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}, ID которое взято при нажатии команды /start {User_id}")

#-------------------------------------------------------------------------------

@router.callback_query(F.data == 'Назад')
async def Back (callback: CallbackQuery):
    await callback.answer('Вы возвращены в меню')
    await callback.message.answer('Вы возвращены в меню', reply_markup = kb.main)