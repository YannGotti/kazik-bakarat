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
from states.userSettings import AdminSettings
from keyboards.inline.admin import *
from keyboards.inline.adminPanel import *
from services.service import *
from config import ADMINS
from handlers.logic.logic import select_updated_data

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.edit_text(ANTI_FLOOD)

@dp.message_handler(commands=['admin'], user_id=ADMINS)
@dp.throttled(anti_flood, rate=0)
async def admin_panel(message: types.Message):
    await message.delete()
    await AdminSettings.Admin.set()
    await message.answer("Админ панель", reply_markup = await getAdminPanelButtons())

@dp.callback_query_handler(adminData.filter(action=["stopGame", "startGame"]), state=AdminSettings.Admin)
async def close_bet(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    action = callback_data['action']

    if action == "stopGame":

        color_win = getColorWin()

        for chat_id in getChatsId():
            color_user = getColorBetUser(chat_id)
            message_id = getMessageId(chat_id)

            if color_win == color_user:
                win_bet = int(getBetUser(chat_id)) * 2
            else:
                win_bet = 0

            updateMoney(chat_id, win_bet)

            if message_id != 0:
                await bot.edit_message_text(chat_id= chat_id, message_id= message_id, text= await select_updated_data(
                    chat_id,
                    BET_CLOSE_USER + f" <b>{color_win}</b>\n" \
                    f"Ваш выигрыш <b>$ {win_bet}</b>"),
                reply_markup= await getBetsKeyboard())

        Closebet()
        await call.message.edit_text("Ставки закрыты", reply_markup = await getAdminPanelButtons())

    if action == "startGame":
        OpenBet()
        await call.message.edit_text("Ставки открыты", reply_markup = await getAdminPanelButtons())


@dp.callback_query_handler(adminData.filter(action=["♦", "❇", "♣"]), state=AdminSettings.Admin)
async def win_color(call: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    color_bet = callback_data['action']
    setColorWin(color_bet)
    await call.message.edit_text(f"Цвет изменен на {color_bet}", reply_markup = await getAdminPanelButtons())
    await call.answer()

@dp.callback_query_handler(adminData.filter(action="exit"), state=AdminSettings.Admin)
async def exit_admin_panel(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Вышел из админки")
    await state.finish()


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True