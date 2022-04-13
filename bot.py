import asyncio
import io
import logging
import os
import telebot

from dotenv import load_dotenv
from iamtoken import gettoken
from speech import synthesize
from telebot.async_telebot import AsyncTeleBot

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

load_dotenv()
bot = AsyncTeleBot(os.getenv('TELEGRAM_API_KEY'))
iamtoken = gettoken(os.getenv('YANDEX_OAUTH_TOKEN'))


@bot.message_handler(commands=['start'])
async def start_bot(message):
    await bot.send_message(message.chat.id, "Hello! Send me something and I will say it.")


@bot.message_handler(commands=['help'])
async def on_help(message):
    await bot.send_message(message.chat.id, "Just send me something and I will pronounce it.")


@bot.message_handler()
async def on_message(message):
    await bot.send_message(message.chat.id, "Give me a moment, recording in progress...")
    strm = io.BytesIO()
    for content in synthesize(os.getenv('YANDEX_FOLDER_ID'), iamtoken, message.text):
        strm.write(content)
    await bot.send_voice(message.chat.id, strm.getbuffer())


async def polling():
    global iamtoken
    while True:
        await asyncio.sleep(3600)
        iamtoken = gettoken(os.getenv('YANDEX_OAUTH_TOKEN'))


async def main():
    await asyncio.gather(bot.infinity_polling(), polling())


asyncio.run(main())
