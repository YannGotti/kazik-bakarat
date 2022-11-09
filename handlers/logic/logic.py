import os

import typing

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData

from loader import dp, bot
from messages import *

from keyboards.default.user import getUserKeyboard

from states.userSettings import UserSetting
from keyboards.inline.admin import *

from services.service import *

async def anti_flood_callback(*args, **kwargs):
    call = args[0]
    chat_id = call.message.chat.id
    await call.message.edit_text(await select_updated_data(chat_id, ANTI_FLOOD), reply_markup = await getBetsKeyboard())
    await call.answer()

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.edit_text(ANTI_FLOOD)

@dp.message_handler(Text(equals=["/play"]), state=None)
@dp.throttled(anti_flood, rate=1)
async def user_connect(message: types.Message):
    await message.delete()

    if not userExists(message.chat.id):
        await message.answer(NOT_REGISTER)
        return

    await message.answer(IN_GAME, reply_markup=await getPlayKeyboard())

@dp.callback_query_handler(gameData.filter(action="play"), state=None)
async def play_game(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    if getMoneyUserInteger(chat_id) < 1000:
        updateMoney(chat_id, 1000)

    if getBetUser(call.message.chat.id) == 0:
        startGameUser(chat_id, call.message.message_id)
    else: 
        setMessageIdUser(call.message.chat.id, call.message.message_id)
    
    await call.message.edit_text(await select_updated_data(chat_id, IF_BET_SETUP), reply_markup = await getBetsKeyboard())
    await UserSetting.IsGaming.set()

@dp.callback_query_handler(gameData.filter(action=["♦", "❇", "♣"]), state=UserSetting.IsGaming)
@dp.throttled(anti_flood_callback, rate=1)
async def red_bet(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    chat_id = call.message.chat.id
    setMessageIdUser(chat_id, call.message.message_id)

    if not isBetStarted():
        await call.message.edit_text(await select_updated_data(chat_id, BETS_NOT_OPEN), reply_markup = await getBetsKeyboard())
        await call.answer()
        return

    selected_color = callback_data['action']
    color_db = getColorBetUser(chat_id)

    if color_db == "Нет" or color_db == selected_color:
        setColorBetUser(chat_id, selected_color)
        await call.message.edit_text(await select_updated_data(chat_id, UP_BET), reply_markup = await getBetsValuesKeyboard())
        await call.answer()
        return

    if selected_color != color_db:
        await call.message.edit_text(await select_updated_data(chat_id, COLOR_BET_SELECTED), reply_markup = await getBetsKeyboard())
        await call.answer()
        return


# TODO UP_BET

@dp.callback_query_handler(gameData.filter(action=["100", "1000", "10000"]), state=UserSetting.IsGaming)
async def up_bet(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    chat_id = call.message.chat.id
    setMessageIdUser(chat_id, call.message.message_id)
    bet = callback_data['action']

    if getMoneyUserInteger(chat_id) < int(bet):
        await call.message.edit_text(await select_updated_data(chat_id, NOT_MONEY_USER), reply_markup = await getBetsKeyboard())
        await call.answer()
        return

    updateBetUser(chat_id, int(bet))
    await call.message.edit_text(await select_updated_data(chat_id, BET_IS_UP), reply_markup = await getBetsKeyboard())
    await call.answer()


@dp.callback_query_handler(gameData.filter(action="ALL"), state=UserSetting.IsGaming)
async def all_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    setMessageIdUser(chat_id, call.message.message_id)

    allBetUser(chat_id)
    await call.message.edit_text(await select_updated_data(chat_id, BET_IS_UP), reply_markup = await getBetsKeyboard())
    await call.answer()

@dp.callback_query_handler(gameData.filter(action="custom"), state=UserSetting.IsGaming)
async def custom_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    
    await state.finish()
    await UserSetting.CustomBetUser.set()
    
    await call.message.edit_text(INPUT_BET)
    await call.answer()

@dp.message_handler(state=UserSetting.CustomBetUser)
async def input_bet(message: types.Message, state: FSMContext):
    await message.delete()
    chat_id = message.chat.id

    try:
        bet = int(message.text)
    except:
        await message.answer(ERROR_UNPUT_BET)
        return

    if getMoneyUserInteger(chat_id) < int(bet):
        await message.answer(await select_updated_data(chat_id, NOT_MONEY_USER), reply_markup = await getBetsKeyboard())
        await state.finish()
        await UserSetting.IsGaming.set()
        return

    updateBetUser(chat_id, int(bet))
    mess = await message.answer(await select_updated_data(chat_id, BET_IS_UP), reply_markup = await getBetsKeyboard())

    setMessageIdUser(chat_id, mess.message_id)

    await state.finish()
    await UserSetting.IsGaming.set()
    

async def select_updated_data(chat_id, invalidate = " "):
    twitch_name = getTwitchName(chat_id)
    money_user = getMoneyUserString(chat_id)
    color_bet = getColorBetUser(chat_id)
    bet = getBetUser(chat_id)

    DATA = f"<b>Пользователь {twitch_name}\n" \
            f"Депозит {money_user}</b>\n" \
            f"Цвет ставки <b>{color_bet}</b>\n" \
            f"Ставка <b>$ {bet}</b>\n\n"\
            f"<b>{invalidate}</b>"
    return DATA

@dp.callback_query_handler(gameData.filter(action="back"), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    bet = int(getBetUser(chat_id))

    if bet == 0:
        setColorBetUser(chat_id, "Нет")
    
    await call.message.edit_text(await select_updated_data(chat_id), reply_markup = await getBetsKeyboard())


@dp.callback_query_handler(gameData.filter(action="cancel"), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, state: FSMContext):
    if getBetUser(call.message.chat.id) == 0:
        stopGameUser(call.message.chat.id)
    else: 
        setMessageIdUser(call.message.chat.id)

    await call.message.edit_text("Вы вышли из игры", reply_markup = await getPlayKeyboard())
    await state.finish()


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True