import logging

from aiogram import Bot

from data.config import ADMINS


async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            bot_properties = await bot.me()
            message = ["<b>Bot ishga tushdi.</b>\n"]
            await bot.send_message(int(admin), "\n".join(message))
        except Exception as err:
            logging.exception(err)
