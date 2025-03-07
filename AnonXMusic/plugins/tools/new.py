import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from AnonXMusic.utils.decorators import AdminActual
from config import BANNED_USERS, adminlist
from AnonXMusic import app

delay_times = {}
authorized_users = {}

@app.on_message(filters.command("setdelay") & filters.group & ~BANNED_USERS)
@AdminActual
async def set_delay(client: Client, message: Message):
    try:
        delay = int(message.command[1])
        if delay < 1:
            return await message.reply("Delay time must be at least 1 minute.")
        chat_id = message.chat.id
        delay_times[chat_id] = delay
        await message.reply(f"Auto-deletion delay set to {delay} minutes.")
    except (IndexError, ValueError):
        await message.reply("Usage: /setdelay <time_in_minutes>")

@app.on_message(filters.command("auth") & filters.group & ~BANNED_USERS)
@AdminActual
async def authorize_user(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply("Reply to a user or provide their user ID.")
    user = await extract_user(message)
    token = await int_to_alpha(user.id)
    _check = await get_authuser_names(message.chat.id)
    count = len(_check)
    if count >= 25:
        return await message.reply("This group has reached the maximum limit of 25 authorized users.")
    if token not in _check:
        assis = {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        }
        get = adminlist.get(message.chat.id)
        if get:
            if user.id not in get:
                get.append(user.id)
        await save_authuser(message.chat.id, token, assis)
        return await message.reply(f"{user.first_name} has been authorized to send media in this group.")
    else:
        return await message.reply(f"{user.first_name} is already authorized.")

@app.on_message(filters.command("unauth") & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthorize_user(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply("Reply to a user or provide their user ID.")
    user = await extract_user(message)
    token = await int_to_alpha(user.id)
    _check = await get_authuser_names(message.chat.id)
    if token in _check:
        await remove_authuser(message.chat.id, token)
        get = adminlist.get(message.chat.id)
        if get:
            if user.id in get:
                get.remove(user.id)
        return await message.reply(f"{user.first_name} has been unauthorized.")
    else:
        return await message.reply(f"{user.first_name} is not authorized.")

@app.on_message(filters.command("authuserlist") & filters.group & ~BANNED_USERS)
@AdminActual
async def list_authorized_users(client: Client, message: Message):
    _check = await get_authuser_names(message.chat.id)
    if _check:
        user_list = "\n".join([f"• {user['auth_name']} (ID: {user['auth_user_id']})" for user in _check.values()])
        return await message.reply(f"Authorized users in this group:\n{user_list}")
    else:
        return await message.reply("No authorized users in this group.")

@app.on_message(filters.group & (
    filters.photo | filters.video | filters.animation | filters.sticker | filters.voice | filters.document
) & ~BANNED_USERS)
async def handle_media(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    _check = await get_authuser_names(chat_id)
    is_admin = user_id in adminlist.get(chat_id, [])
    is_authorized = str(user_id) in _check
    if is_admin or is_authorized:
        return
    if chat_id in delay_times:
        delay = delay_times[chat_id]
        await asyncio.sleep(delay * 60)
        try:
            await message.delete()
            print(f"Deleted media in chat {chat_id} after {delay} minutes.")
        except Exception as e:
            print(f"Failed to delete media: {e}")

async def extract_user(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    else:
        user_id = message.command[1]
        return await app.get_users(user_id)

async def int_to_alpha(user_id: int):
    return str(user_id)

async def get_authuser_names(chat_id: int):
    return authorized_users.get(chat_id, {})

async def save_authuser(chat_id: int, token: str, data: dict):
    if chat_id not in authorized_users:
        authorized_users[chat_id] = {}
    authorized_users[chat_id][token] = data

async def remove_authuser(chat_id: int, token: str):
    if chat_id in authorized_users and token in authorized_users[chat_id]:
        del authorized_users[chat_id][token]
