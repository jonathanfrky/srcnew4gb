#devggn


from pyrogram import filters, Client
from devgagan import app
from pyromod import listen
import random
import os
import string
from devgagan.core.mongo import db
from devgagan.core.func import subscribe, chk_user
from config import API_ID as api_id, API_HASH as api_hash
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)

def generate_random_name(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))  # Editted ... 

async def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    memory_file = f"session_{user_id}.session-journal"

    session_file_exists = os.path.exists(session_file)
    memory_file_exists = os.path.exists(memory_file)

    if session_file_exists:
        os.remove(session_file)
    
    if memory_file_exists:
        os.remove(memory_file)

    # Delete session from the database
    if session_file_exists or memory_file_exists:
        await db.delete_session(user_id)
        return True  # Files were deleted
    return False  # No files found

@app.on_message(filters.command("chiqish"))
async def clear_db(client, message):
    user_id = message.chat.id
    files_deleted = await delete_session_files(user_id)

    if files_deleted:
        await message.reply("✅ Sizning ma'lumotlaringiz va fayllaringiz xotiradan o'chirildi.")
    else:
        await message.reply("⚠️ Siz tizimga hali kirmagansiz.")
        
    
@app.on_message(filters.command("kirish"))
async def generate_session(_, message):
    joined = await subscribe(_, message)
    if joined == 1:
        return
        
    # user_checked = await chk_user(message, message.from_user.id)
    # if user_checked == 1:
        # return
        
    user_id = message.chat.id   
    
    number = await _.ask(user_id, 'Iltimos, telefon raqamingizni mamlakat kodi bilan birga kiriting. \nMasalan: +998901234567', filters=filters.text)   
    phone_number = number.text
    try:
        await message.reply("📲 Kod yuborilmoqda...")
        client = Client(f"session_{user_id}", api_id, api_hash)
        
        await client.connect()
    except Exception as e:
        await message.reply(f"❌ Kod yuborishda xatolik {e}. Iltimos keyinroq qayta urinib ko‘ring.")
    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        await message.reply('❌ API ID va API HASH kombinatsiyasi noto‘g‘ri. Iltimos, boshidan qayta boshlang.')
        return
    except PhoneNumberInvalid:
        await message.reply("❌ Noto'g'ri raqam. Iltimos, boshidan qayta boshlang.")
        return
    try:
        otp_code = await _.ask(user_id, "Telegramdan sizga kod kelganini tekshiring. Kelgan taqdirda, uni quyidagi formatda kiriting: \nMasalan sizga `12345` raqamli kod keldi, siz ularni joy tashlab kiriting `1 2 3 4 5`.", filters=filters.text, timeout=600)
    except TimeoutError:
        await message.reply('⏰ 10 daqiqalik vaqt chegarasidan oshib ketdi. Iltimos, sessiyani qayta ishga tushiring.')
        return
    phone_code = otp_code.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
                
    except PhoneCodeInvalid:
        await message.reply('❌ Yaroqsiz kod. Iltimos, boshidan qayta boshlang.')
        return
    except PhoneCodeExpired:
        await message.reply('❌ Eskirgan kod. Iltimos, boshidan qayta boshlang.')
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await _.ask(user_id, 'Hisobingizda ikki bosqichli tasdiqlash yoqilgan. Iltimos, parolingizni kiriting. (jarayon xavfsiz, biz malumotlaringizga egalik qilmaymiz!)', filters=filters.text, timeout=300)
        except TimeoutError:
            await message.reply('⏰ 5 daqiqalik vaqt chegarasidan oshib ketdi. Iltimos, boshidan qayta boshlang.')
            return
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('❌ Parolingizni xato kiritdingiz. Iltimos, boshidan qayta boshlang.')
            return
    string_session = await client.export_session_string()
    await db.set_session(user_id, string_session)
    await client.disconnect()
    await otp_code.reply("✅ Muvaffaqqiyatli kirish amalga oshdi!")
