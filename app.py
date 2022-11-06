import logging

from aiogram.types import BotCommand

from loader import bot, storage
from services.service import *


async def set_default_commands(dp_local):
    await dp_local.bot.set_my_commands([
        BotCommand("change_twitch", "Поменять никнейм Twitch"),
        BotCommand("menu", "Вызвать меню")
    ])


async def on_shutdown():
    await storage.close()
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    # generate_lotteries_in_file(1000, "lotteries.txt")
    # generate_images_if_not_exists_from_file("lotteries.txt")
    #addGame()

    executor.start_polling(dp, on_shutdown=on_shutdown, skip_updates=True, on_startup=set_default_commands)
