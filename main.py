import asyncio
import os
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from dotenv import load_dotenv

load_dotenv()

JIVO_CHAT_ID = int(os.getenv("JIVO_CHAT_ID"))
JIVO_BOT = int(os.getenv("JIVO_BOT"))
api_id = str(os.getenv("APP_ID"))
api_hash = str(os.getenv("API_HASH"))

proxy = {"scheme": "http", "host": "192.168.152.200", "port": 8080}
app = Client("my_account", api_id, api_hash, proxy=proxy)


def extract_message_id(text):
    # extract message id from text like "#123456789 text"
    if text.startswith("#"):
        message_id = text.split(" ", 1)[0][1:]
        if message_id.isdigit():
            return int(message_id)
    return None


def extract_text(text):
    # extract text without message id from text like "#123456789 text"
    if text.startswith("#"):
        text = text.split(" ", 1)[1]
    return text


@app.on_message()
async def my_handler(client, message: Message):
    if message.chat.id == JIVO_CHAT_ID:
        if message.from_user:
            text = f"#{message.id} {message.from_user.first_name or ''} {message.from_user.last_name or ''} " \
                   f"{message.from_user.username or ''} \n{message.text}"
            await client.send_message(JIVO_BOT, text)
    if message.chat.id == JIVO_BOT:
        text = message.text
        message_id = extract_message_id(text)
        text = extract_text(text)
        await client.send_message(JIVO_CHAT_ID, text, reply_to_message_id=message_id)


async def main():
    print(JIVO_CHAT_ID, JIVO_BOT, api_id, api_hash)
    async with app:
        async for dialog in app.get_dialogs(limit=10):
            print(dialog.chat.title or dialog.chat.first_name, dialog.chat.id)


app.run(main())
