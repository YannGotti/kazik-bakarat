import os

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext

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
    await call.message.edit_text(await select_updated_data(chat_id), reply_markup = await getBetsKeyboard())
    await UserSetting.IsGaming.set()

@dp.callback_query_handler(gameData.filter(action="red"), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    color_selected = getColorBetUser(chat_id)

    if not color_selected == "♦":
        await call.message.edit_text(await select_updated_data(chat_id, COLOR_BET_SELECTED), reply_markup = await getBetsKeyboard())
        await call.answer()
    
    if color_selected == "Нет" or color_selected == "♦":
        setColorBetUser(chat_id, "♦")
        await call.message.edit_text(await select_updated_data(chat_id, UP_BET), reply_markup = await getBetsValuesKeyboard())
        await call.answer()

@dp.callback_query_handler(gameData.filter(action="blue"), state=UserSetting.IsGaming)
async def blue_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    color_selected = getColorBetUser(chat_id)

    if not color_selected == "♣":
        await call.message.edit_text(await select_updated_data(chat_id, COLOR_BET_SELECTED), reply_markup = await getBetsKeyboard())
        await call.answer()

    
    if color_selected == "Нет" or color_selected == "♣":
        setColorBetUser(chat_id, "♣")
        await call.message.edit_text(await select_updated_data(chat_id, UP_BET), reply_markup = await getBetsValuesKeyboard())
        await call.answer()

@dp.callback_query_handler(gameData.filter(action="green"), state=UserSetting.IsGaming)
async def green_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    color_selected = getColorBetUser(chat_id)

    if not color_selected == "❇":
        await call.message.edit_text(await select_updated_data(chat_id, COLOR_BET_SELECTED), reply_markup = await getBetsKeyboard())
        await call.answer()

    if color_selected == "Нет" or color_selected == "❇":
        setColorBetUser(chat_id, "❇")
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

@dp.callback_query_handler(gameData.filter(action="100"), state=UserSetting.IsGaming)
async def up_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    updateBetUser(chat_id, 100)
    await call.message.edit_text(await select_updated_data(chat_id, BET_IS_UP), reply_markup = await getBetsKeyboard())
    await call.answer()


@dp.callback_query_handler(gameData.filter(action="1000"), state=UserSetting.IsGaming)
async def up_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    updateBetUser(chat_id, 1000)
    await call.message.edit_text(await select_updated_data(chat_id, BET_IS_UP), reply_markup = await getBetsKeyboard())
    await call.answer()

@dp.callback_query_handler(gameData.filter(action="10000"), state=UserSetting.IsGaming)
async def up_bet(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    updateBetUser(chat_id, 10000)
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