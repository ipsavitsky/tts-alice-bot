import asyncio
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from speech import synthesize
from iamtoken import gettoken
import os
import io

# params = ConfigParser()
# params.read('config.cfg')
load_dotenv()

bot = AsyncTeleBot(os.getenv('TELEGRAM_API_KEY'))

iamtoken = gettoken(os.getenv('YANDEX_OAUTH_TOKEN'))

@bot.message_handler(commands=['start', 'help'])
async def start_bot(message):
    pass

@bot.message_handler()
async def on_message(message):
    await bot.send_message(message.chat.id, "Записываю голосовую...")
    strm = io.BytesIO()
    
    for content in synthesize(os.getenv('YANDEX_FOLDER_ID'), iamtoken, message.text):
        strm.write(content)
    await bot.send_voice(message.chat.id, strm.getbuffer())



async def polling():
    global iamtoken
    while True:
        await asyncio.sleep(3600)
        # print("switching token...")
        iamtoken = gettoken(os.getenv('YANDEX_OAUTH_TOKEN'))

async def main():
    await asyncio.gather(bot.infinity_polling(), polling())


asyncio.run(main())