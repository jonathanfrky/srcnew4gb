#devgaganin

from datetime import timedelta
import pytz
import datetime, time
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import get_seconds
from devgagan.core.mongo import plans_db  
from pyrogram import filters 



@app.on_message(filters.command("rem") & filters.user(OWNER_ID))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  
        user = await client.get_users(user_id)
        data = await plans_db.check_premium(user_id)  
        
        if data and data.get("_id"):
            await plans_db.remove_premium(user_id)
            await message.reply_text("Foydalanuvchi muvaffaqqiyatli olib tashlandi!")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜᴇʏ {user.mention},\n\nSizning premiumga kirish imkoniyatingiz olib tashlandi.\nXizmatdan foydalanganingiz uchun rahmat 😊.</b>"
            )
        else:
            await message.reply_text("Foydalanuvchini olib tashlashda xatolik!\nFoydalanuvchi premium ekanligiga ishonchingiz komilmi?")
    else:
        await message.reply_text("Foydalanish : /rem user_id") 



@app.on_message(filters.command("rejam"))
async def myplan(client, message):
    user_id = message.from_user.id
    user = message.from_user.mention
    data = await plans_db.check_premium(user_id)  
    if data and data.get("expire_date"):
        expiry = data.get("expire_date")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Tashkent"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Tashkent")).strftime("%d-%m-%Y\n⏱️ Tugash vaqt : %I:%M:%S %p")            
        
        current_time = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
        time_left = expiry_ist - current_time
            
        
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        
        time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"
        await message.reply_text(f"⚜️ Premium foydalanuvchi ma'lumoti :\n\n👤 Foydalanuvchi : {user}\n⚡ User ID : <code>{user_id}</code>\n⏰ Qolgan vaqt : {time_left_str}\n⌛️ Tugash vaqt : {expiry_str_in_ist}")   
    else:
        await message.reply_text(f"Hey {user},\n\nSizda hech qanday premium reja mavjud emas!")
        


@app.on_message(filters.command("tekshirish") & filters.user(OWNER_ID))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await plans_db.check_premium(user_id)  
        if data and data.get("expire_date"):
            expiry = data.get("expire_date") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Tashkent"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Tashkent")).strftime("%d-%m-%Y\n⏱️ Tugash vaqt : %I:%M:%S %p")            
            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
            time_left = expiry_ist - current_time
            
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"⚜️ Premium foydalanuvchi ma'lumoti :\n\n👤 Foydalanuvchi : {user.mention}\n⚡ User ID : <code>{user_id}</code>\n⏰ Qolgan vaqt : {time_left_str}\n⌛️ Tugash vaqt : {expiry_str_in_ist}")
        else:
            await message.reply_text("Hech qanday premium ma'lumotlari topilmadi!")
    else:
        await message.reply_text("Foydalanish : /tekshirish user_id")


@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ Ulanish vaqti : %I:%M:%S %p") 
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)  
            await plans_db.add_premium(user_id, expiry_time)  
            data = await plans_db.check_premium(user_id)
            expiry = data.get("expire_date")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Tashkent")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")         
            await message.reply_text(f"Premiumga muvaffaqqiyatli qo'shildi ✅\n\n👤 Foydalanuvchi : {user.mention}\n⚡ User ID : <code>{user_id}</code>\n⏰ Premium ruxsat : <code>{time}</code>\n\n⏳ Ulnaish vaqti : {current_time}\n\n⌛️ Tugash vaqt : {expiry_str_in_ist}\n\n__**Powered by @jonathanfrky__**", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"👋 Hey {user.mention},\nSiz premiumga ega bo'ldingiz.\nMaza qiling !! ✨🎉\n\n⏰ Premium ruxsati: <code>{time}</code>\n⏳ Ulangan vaqtingiz : {current_time}\n\n⌛️ Tugash vaqti : {expiry_str_in_ist}", disable_web_page_preview=True              
            )    
#            await client.send_message(PREMIUM_LOGS, text=f"#Added_Premium\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True)
                    
        else:
            await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year'")
    else:
        await message.reply_text("Usage : /add user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')")

  
