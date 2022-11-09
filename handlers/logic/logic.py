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

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.answer("Защита от спама, подождите 25 сек")

@dp.callback_query_handler(gameData.filter(action="play"), state=None)
async def play_game(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    startGameUser(chat_id)
    await call.message.edit_text(await select_updated_data(chat_id, IF_BET_SETUP), reply_markup = await getBetsKeyboard())
    await UserSetting.IsGaming.set()

@dp.callback_query_handler(gameData.filter(action=["♦", "❇", "♣"]), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    chat_id = call.message.chat.id

    if not isBetStarted():
        await call.message.edit_text(await select_updated_data(chat_id, BETS_NOT_OPEN), reply_markup = await getBetsKeyboard())
        await call.answer()
        return

    selected_color = callback_data['action']
    color_selected = getColorBetUser(chat_id)

    if not color_selected == selected_color:
        await call.message.edit_text(await select_updated_data(chat_id, COLOR_BET_SELECTED), reply_markup = await getBetsKeyboard())
    
    if color_selected == "Нет" or color_selected == selected_color:
        setColorBetUser(chat_id, selected_color)
        await call.message.edit_text(await select_updated_data(chat_id, UP_BET), reply_markup = await getBetsValuesKeyboard())

    await call.answer()


@dp.callback_query_handler(gameData.filter(action="back"), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    setColorBetUser(chat_id, "Нет")
    await call.message.edit_text(await select_updated_data(chat_id), reply_markup = await getBetsKeyboard())


@dp.callback_query_handler(gameData.filter(action="cancel"), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, state: FSMContext):
    setColorBetUser(call.message.chat.id, "Нет")
    await call.message.edit_text("Вы вышли из игры", reply_markup = await getPlayKeyboard())
    await state.finish()


# TODO UP_BET

@dp.callback_query_handler(gameData.filter(action=["100", "1000", "10000"]), state=UserSetting.IsGaming)
async def up_bet(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    chat_id = call.message.chat.id
    bet = callback_data['action']

    updateBetUser(chat_id, int(bet))
    await call.message.edit_text(await select_updated_data(chat_id, BET_IS_UP), reply_markup = await getBetsKeyboard())
    await call.answer()


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


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True