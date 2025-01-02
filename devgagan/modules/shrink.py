from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AD_API # you can edit this by any short link provider

# MongoDB setup
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["srcnew"]
token = tdb["tokens"]

# Create a TTL index for sessions collection
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)


# In-memory parameter storage
Param = {}


async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
    
    # Use aiohttp to perform an asynchronous request
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()  # Get the JSON response asynchronously
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None


async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None


@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """/token buyrug'ini boshqaring."""
    join = await subscribe(client, message)
    if join == 1:
        return
    user_id = message.chat.id
    if len(message.command) <= 1:
        image_url = "https://github.com/ae010108/app1/blob/main/ayw.jpg?raw=true"
        join_button = InlineKeyboardButton("Administrator ⚡️", url="https://t.me/jonathanfrky")
        premium = InlineKeyboardButton("Musiqa kanal 🎶", url="https://t.me/joninmusic")  # Callback for Help button
        keyboard = InlineKeyboardMarkup([
            [join_button,  # First button
            premium]   # Second button
        ])
        # Send the message with the image and keyboard
        await message.reply_photo(
            photo=image_url,
            caption=(
                "Salom 👋\n"
                "✳️ Men orqali siz uzatish cheklangan kanal/guruhlardan postlarni saqlab olishingiz mumkin. YT, INSTA, ... ijtimoiy platformalardan video/audio yuklab olishim mumkin\n"
                "✳️ Ommaviy kanallar uchun shunchaki post linkini yuboring. Shaxsiy kanallar uchun, avval /kirish orqali botga kiring, keyin post havolasini yuboring. Yordam uchun /yordam buyrug'ini yuboring\n\n"
                "> Diqqat ushbu botdagi barcha harakatlaringizga o'zingiz javob berasiz! Botni keyinchalik ishlatish mobaynida ushbu qoidaga rozi ekanligingizni bildirasiz! Boshlashdan avval /shartlar buyrug'ini yuborib tanishib chiqing!!!"
                 ),
            reply_markup=keyboard
        )
        return  
        
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("Siz premium foydalanuvchisiz, token kerak emas 😉")
        return

    # Handle deep link with parameter
    if param:
        if user_id in Param and Param[user_id] == param:
            # Add user to MongoDB as a verified user for the next 6 hours
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]  # Remove the parameter from Param
            await message.reply("✅ Siz muvaffaqiyatli tekshirildingiz! Keyingi 3 soat davomida seansingizdan rohatlaning.")
            return
        else:
            await message.reply("❌ Tasdiqlash havolasi yaroqsiz yoki muddati o‘tgan. Iltimos, yangi token yarating.")
            return

@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
    # Check if the user is already verified or premium
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("Siz premium foydalanuvchisiz, token kerak emas 😉")
        return
    if await is_user_verified(user_id):
        await message.reply("✅ Bepul seansingiz allaqachon faol, zavqlaning!!")
    else:
        # Generate a session and send the link
        param = await generate_random_param()
        Param[user_id] = param  # Store the parameter in Param dictionary

        # Create a deep link
        deep_link = f"https://t.me/{client.me.username}?start={param}"

        # Get shortened URL
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Token havolasini yaratib bo‘lmadi. Iltimos, qayta urinib koʻring.")
            return

        # Create a button with the shortened link
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Tokenni hozir tasdiqlang...", url=shortened_url)]]
        )
        await message.reply("Bepul kirish tokeningizni tasdiqlash uchun quyidagi tugmani bosing: \n\n> Sizga nima beriladi? \n1. 3 soatgacha vaqt cheklanmagan \n2. To'plamli buyruqlar chegarasi FreeLimit + 20 \n3 bo'ladi. Barcha funksiyalar qulfdan chiqarilgan", reply_markup=button)
