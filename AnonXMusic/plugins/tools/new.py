import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from AnonXMusic import app

delay_times = {}
authorized_users = {}

@app.on_message(filters.command("setdelay") & filters.group)
async def set_delay(client: Client, message: Message):
    try:
        user_status = (await message.chat.get_member(message.from_user.id)).status
        if user_status not in ("creator", "administrator"):
            await message.reply("Only admins can set the delay time.")
            return
        delay = int(message.command[1])
        if delay < 1:
            await message.reply("Delay time must be at least 1 minute.")
            return
        chat_id = message.chat.id
        delay_times[chat_id] = delay
        await message.reply(f"Auto-deletion delay set to {delay} minutes.")
    except (IndexError, ValueError):
        await message.reply("Usage: /setdelay <time_in_minutes>")

@app.on_message(filters.command("auth") & filters.group)
async def authorize_user(client: Client, message: Message):
    try:
        user_status = (await message.chat.get_member(message.from_user.id)).status
        if user_status not in ("creator", "administrator"):
            await message.reply("Only admins can authorize users.")
            return
        user_id = int(message.command[1])
        chat_id = message.chat.id
        if chat_id not in authorized_users:
            authorized_users[chat_id] = []
        if user_id not in authorized_users[chat_id]:
            authorized_users[chat_id].append(user_id)
            await message.reply(f"User {user_id} has been authorized.")
        else:
            await message.reply(f"User {user_id} is already authorized.")
    except (IndexError, ValueError):
        await message.reply("Usage: /auth <user_id>")

@app.on_message(filters.command("unauth") & filters.group)
async def unauthorize_user(client: Client, message: Message):
    try:
        user_status = (await message.chat.get_member(message.from_user.id)).status
        if user_status not in ("creator", "administrator"):
            await message.reply("Only admins can unauthorize users.")
            return
        user_id = int(message.command[1])
        chat_id = message.chat.id
        if chat_id in authorized_users and user_id in authorized_users[chat_id]:
            authorized_users[chat_id].remove(user_id)
            await message.reply(f"User {user_id} has been unauthorized.")
        else:
            await message.reply(f"User {user_id} is not authorized.")
    except (IndexError, ValueError):
        await message.reply("Usage: /unauth <user_id>")

@app.on_message(filters.command("authuserlist") & filters.group)
async def list_authorized_users(client: Client, message: Message):
    try:
        user_status = (await message.chat.get_member(message.from_user.id)).status
        if user_status not in ("creator", "administrator"):
            await message.reply("Only admins can view the authorized users list.")
            return
        chat_id = message.chat.id
        if chat_id in authorized_users and authorized_users[chat_id]:
            user_list = "\n".join(str(user_id) for user_id in authorized_users[chat_id])
            await message.reply(f"Authorized users in this group:\n{user_list}")
        else:
            await message.reply("No authorized users in this group.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@app.on_message(filters.group & (
    filters.photo | filters.video | filters.animation | filters.sticker | filters.voice | filters.document
))
async def handle_media(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_status = (await message.chat.get_member(user_id)).status
    is_admin = user_status in ("creator", "administrator")
    is_authorized = chat_id in authorized_users and user_id in authorized_users[chat_id]
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
