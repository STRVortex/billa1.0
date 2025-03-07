import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from AnonXMusic import app

mongo_client = MongoClient("mongodb+srv://kunaalkumar0091:6qhyyQIyS2idoGFQ@cluster0.z2jge.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["media_bot_db"]
authorized_users_collection = db["authorized_users"]

delay_times = {}

@app.on_message(filters.command("setdelay") & filters.group)
async def set_delay(client: Client, message: Message):
    if not await is_admin(client, message):
        await message.reply("Only admins can use this command.")
        return
    try:
        delay = int(message.command[1])
        if delay < 1:
            await message.reply("Delay time must be at least 1 minute.")
            return
        chat_id = message.chat.id
        delay_times[chat_id] = delay
        await message.reply(f"Auto-deletion delay set to {delay} minutes.")
    except (IndexError, ValueError):
        await message.reply("Usage: /setdelay <time_in_minutes>")

@app.on_message(filters.command("mauth") & filters.group)
async def authorize_user(client: Client, message: Message):
    if not await is_admin(client, message):
        await message.reply("Only admins can use this command.")
        return
    try:
        user_id = int(message.command[1])
        chat_id = message.chat.id
        authorized_users_collection.update_one(
            {"chat_id": chat_id},
            {"$addToSet": {"authorized_users": user_id}},
            upsert=True
        )
        await message.reply(f"User {user_id} has been authorized in this group.")
    except (IndexError, ValueError):
        await message.reply("Usage: /mauth <user_id>")

@app.on_message(filters.command("munauth") & filters.group)
async def unauthorize_user(client: Client, message: Message):
    if not await is_admin(client, message):
        await message.reply("Only admins can use this command.")
        return
    try:
        user_id = int(message.command[1])
        chat_id = message.chat.id
        authorized_users_collection.update_one(
            {"chat_id": chat_id},
            {"$pull": {"authorized_users": user_id}}
        )
        await message.reply(f"User {user_id} has been unauthorized in this group.")
    except (IndexError, ValueError):
        await message.reply("Usage: /munauth <user_id>")

@app.on_message(filters.command("mauthuserslist") & filters.group)
async def list_authorized_users(client: Client, message: Message):
    if not await is_admin(client, message):
        await message.reply("Only admins can use this command.")
        return
    chat_id = message.chat.id
    result = authorized_users_collection.find_one({"chat_id": chat_id})
    if result and "authorized_users" in result:
        authorized_users = result["authorized_users"]
        if authorized_users:
            users_list = "\n".join([f"`{user_id}`" for user_id in authorized_users])
            await message.reply(f"Authorized users in this group:\n{users_list}")
        else:
            await message.reply("No authorized users in this group.")
    else:
        await message.reply("No authorized users in this group.")

@app.on_message(filters.group & (
    filters.photo | filters.video | filters.animation | filters.sticker | filters.voice | filters.document
))
async def handle_media(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_authorized = await is_user_authorized(chat_id, user_id)
    is_admin = await is_admin(client, message)
    if is_authorized or is_admin:
        return
    if chat_id in delay_times:
        delay = delay_times[chat_id]
        await asyncio.sleep(delay * 60)
        try:
            await message.delete()
            print(f"Deleted media in chat {chat_id} after {delay} minutes.")
        except Exception as e:
            print(f"Failed to delete media: {e}")

async def is_admin(client: Client, message: Message) -> bool:
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception as e:
        print(f"Failed to check admin status: {e}")
        return False

async def is_user_authorized(chat_id: int, user_id: int) -> bool:
    result = authorized_users_collection.find_one(
        {"chat_id": chat_id, "authorized_users": user_id}
    )
    return result is not None
