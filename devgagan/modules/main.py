import time
import random
import string
import asyncio
from pyrogram import filters, Client
from devgagan import app
from config import API_ID, API_HASH, FREEMIUM_LIMIT, PREMIUM_LIMIT, OWNER_ID
from devgagan.core.get_func import get_msg
from devgagan.core.func import *
from devgagan.core.mongo import db
from devgagan.modules.shrink import is_user_verified
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
async def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
users_loop = {}
interval_set = {}
batch_mode = {}
async def check_interval(user_id, freecheck):
    if freecheck != 1 or await is_user_verified(user_id):
        return True, None
    now = datetime.now()
    if user_id in interval_set:
        cooldown_end = interval_set[user_id]
        if now < cooldown_end:
            remaining_time = (cooldown_end - now).seconds // 60
            return False, f"Iltimos {remaining_time} minut kuting. Boshqa link jo'natishdan oldin.Shu bilan bir qatorda, tezkor kirish uchun premium xarid qiling.\n\n> Salom 👋 Siz /token yordamida botdan 3 soat davomida hech qanday cheklovsiz bepul foydalanishingiz mumkin. "
        else:
            del interval_set[user_id]
    return True, None
async def set_interval(user_id, interval_minutes=5):
    now = datetime.now()
    interval_set[user_id] = now + timedelta(minutes=interval_minutes)
@app.on_message(filters.regex(r'https?://(?:www\.)?t\.me/[^\s]+'))
async def single_link(_, message):
    user_id = message.chat.id
    if user_id in batch_mode:
        return
    if users_loop.get(user_id, False):
        await message.reply(
            "Sizda allaqachon davom etayotgan jarayon bor. Iltimos, uning tugashini kuting yoki /bekor bilan bekor qiling."
        )
        return    
    freecheck = await chk_user(message, user_id)
    if freecheck == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID:
        await message.reply("Hozirda bepul xizmat mavjud emas. Kirish uchun premiumga obuna bo'ling.")
        return
    can_proceed, response_message = await check_interval(user_id, freecheck)
    if not can_proceed:
        await message.reply(response_message)
        return
    users_loop[user_id] = True
    link = get_link(message.text) 
    userbot = None
    try:
        join = await subscribe(_, message)
        if join == 1:
            users_loop[user_id] = False
            return
        msg = await message.reply("Qayta ishlanmoqda...")
        if 't.me/' in link and 't.me/+' not in link and 't.me/c/' not in link and 't.me/b/' not in link:
            await get_msg(None, user_id, msg.id, link, 0, message)
            await set_interval(user_id, interval_minutes=5)
            return
        data = await db.get_data(user_id)
        if data and data.get("session"):
            session = data.get("session")
            try:
                device = 'jonathanfrky'
                session_name = await generate_random_name()
                userbot = Client(session_name, api_id=API_ID, api_hash=API_HASH, device_model=device, session_string=session)
                await userbot.start()                
            except:
                users_loop[user_id] = False
                return await msg.edit_text("Kirish muddati tugadi. Iltimos /kirish buyrug'ini yuborib qayta kiring.")
        else:
            users_loop[user_id] = False
            await msg.edit_text("Shaxsiy kanallardan yuklab olish uchun birinchi botga kirishingiz zarur.\nBuning uchun /kirish buyrug'ini yuboring va ketma-ketlikka amal qiling.")
            return
        try:
            if 't.me/+' in link:
                q = await userbot_join(userbot, link)
                await msg.edit_text(q)
            elif 't.me/c/' in link:
                await get_msg(userbot, user_id, msg.id, link, 0, message)
                await set_interval(user_id, interval_minutes=5)
            else:
                await msg.edit_text("Havola formati noto‘g‘ri.")
        except Exception as e:
            await msg.edit_text(f"Link: `{link}`\n\n**Xatolik:** {str(e)}")
    except FloodWait as fw:
        await msg.edit_text(f"Iltimos {fw.x} sekunddan keyin qayta urinib ko'ring. Telegram tomonidan cheklovlar!")
    except Exception as e:
        await msg.edit_text(f"Link: `{link}`\n\n**Xatolik:** {str(e)}")
    finally:
        if userbot and userbot.is_connected:
            await userbot.stop()
        users_loop[user_id] = False
@app.on_message(filters.command("ommaviy"))
async def batch_link(_, message):
    user_id = message.chat.id
    if users_loop.get(user_id, False):
        await app.send_message(
            message.chat.id,
            "Sizda allaqachon ommaviy jarayon ishlayotgan. Iltimos, yangisini boshlashdan oldin uning tugashini kuting."
        )
        return
    freecheck = await chk_user(message, user_id)
    if freecheck == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID:
        await message.reply("Bepul xizmati hozircha mavjud emas. Kirish uchun premiumga yangilang.")
        return    
    toker = await is_user_verified(user_id)
    if toker:
        max_batch_size = (FREEMIUM_LIMIT + 20)
        freecheck = 0
    else:
        freecheck = await chk_user(message, user_id)
        if freecheck == 1:
            max_batch_size = FREEMIUM_LIMIT
        else:
            max_batch_size = PREMIUM_LIMIT
    
    while True:
        start = await app.ask(message.chat.id, text="Iltimos olmoqchi bo'lgan birinchi postingizni linkini yuboring.")
        start_id = start.text.strip()
        s = start_id.split("/")[-1]
        try:
            cs = int(s)
            break
        except ValueError:
            await app.send_message(message.chat.id, "Yaroqsiz link. Iltimos, yana yuboring ...")
    while True:
        num_messages = await app.ask(message.chat.id, text="Qancha xabarni qayta ishlashni xohlaysiz?")
        try:
            cl = int(num_messages.text.strip())
            if cl <= 0 or cl > max_batch_size:
                raise ValueError(f"Xabarlar soni 1 va {max_batch_size}. orasida bo'lishi kerak")
            break
        except ValueError as e:
            await app.send_message(message.chat.id, f"Yaroqsiz raqam: {e}. Iltimos, yana yaroqli raqamni kiriting ...")
    can_proceed, response_message = await check_interval(user_id, freecheck)
    if not can_proceed:
        await message.reply(response_message)
        return
    join_button = InlineKeyboardButton("Kanalga ulanish", url="https://t.me/jonmvrck")
    keyboard = InlineKeyboardMarkup([[join_button]])
    pin_msg = await app.send_message(
        user_id,
        "Ommaviy yuklab olish boshlandi ⚡\n__Qayta ishlanmoqda: 0/{cl}__\n\n**__Powered by @jonathanfrky__**",
        reply_markup=keyboard
    )
    try:
        await pin_msg.pin()
    except Exception as e:
        await pin_msg.pin(both_sides=True)
    users_loop[user_id] = True
    try:
        for i in range(cs, cs + cl):
            if user_id in users_loop and users_loop[user_id]:
                try:
                    x = start_id.split('/')
                    y = x[:-1]
                    result = '/'.join(y)
                    url = f"{result}/{i}"
                    link = get_link(url)
                    if 't.me/' in link and 't.me/b/' not in link and 't.me/c' not in link:
                        msg = await app.send_message(message.chat.id, f"Processing link {url}...")
                        await get_msg(None, user_id, msg.id, link, 0, message)
                        await pin_msg.edit_text(
                        f"Ommaviy yuklab olish boshlandi ⚡\n__Qayta ishlanmoqda: {i - cs + 1}/{cl}__\n\n**__Powered by @jonathanfrky__**",
                        reply_markup=keyboard
                        )
                        await asyncio.sleep(5)
                except Exception as e:
                    print(f"Havolani qayta ishlashda xatolik yuz berdi {url}: {e}")
                    continue
        if not any(prefix in start_id for prefix in ['t.me/c/', 't.me/b/']):
            await set_interval(user_id, interval_minutes=20)
            await app.send_message(message.chat.id, "Ommaviy yuklab olish muvaffaqqiyatli tugallandi! 🎉")
            await pin_msg.edit_text(
                        f"Ommaviy yulab olish tugallandi {cl} xabarlar olindi 🌝\n\n**__Powered by @jonathanfrky__**",
                        reply_markup=keyboard
            )
            return
        data = await db.get_data(user_id)
        if data and data.get("session"):
            session = data.get("session")
            device = 'jonathanfrky'
            session_name = await generate_random_name()
            userbot = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                device_model=device,
                session_string=session
            )
            await userbot.start()
        else:
            await app.send_message(message.chat.id, "Shaxsiy kanallardan yuklab olish uchun birinchi botga kirishingiz zarur.\nBuning uchun /kirish buyrug'ini yuboring va ketma-ketlikka amal qiling.")
            return
        try:
            for i in range(cs, cs + cl):
                if user_id in users_loop and users_loop[user_id]:
                    try:
                        x = start_id.split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)
                        if 't.me/b/' in link or 't.me/c/' in link:
                            msg = await app.send_message(message.chat.id, f"Linkni qayta ishlab bo'lmadi! Ehtimol post o'chirilgan: {url}")
                            await get_msg(userbot, user_id, msg.id, link, 0, message)
                            sleep_msg = await app.send_message(
                                message.chat.id,
                                "Telegram cheklovlari sabab har bir post 5 sekund ketma-ketligida yuboriladi."
                            )
                            await asyncio.sleep(2)
                            await pin_msg.edit_text(
                            f"Ommaviy yuklab olish boshlandi ⚡\n__Qayta ishlanmoqda: {i - cs + 1}/{cl}__\n\n**__Powered by @jonathanfrky_**",
                            reply_markup=keyboard
                            )
                            await asyncio.sleep(10)
                            await sleep_msg.delete()
                    except Exception as e:
                        print(f"Ushbu linkni qayta ishlashda xatolik {url}: {e}")
                        continue
        finally:
            if userbot.is_connected:
                await userbot.stop()
        await app.send_message(message.chat.id, "Ommaviy yuklab olish muvaffaqqiyatli tugallandi! 🎉")
        await set_interval(user_id, interval_minutes=20)
        await pin_msg.edit_text(
                        f"Ommaviy yuklab olish {cl}ta xabar bilan tugallandi ⚡\n\n**__Powered by @jonathanfrky__**",
                        reply_markup=keyboard
        )
    except FloodWait as fw:
        await app.send_message(
            message.chat.id,
            f"Iltimos {fw.x} sekunddan keyin qayta urinib ko'ring. Telegram tomonidan cheklovlar!."
        )
    except Exception as e:
        await app.send_message(message.chat.id, f"Error: {str(e)}")
    finally:
        users_loop.pop(user_id, None)
@app.on_message(filters.command("bekor"))
async def stop_batch(_, message):
    user_id = message.chat.id
    if user_id in users_loop and users_loop[user_id]:
        users_loop[user_id] = False
        await app.send_message(
            message.chat.id, 
            "To'plamni qayta ishlash muvaffaqiyatli to'xtatildi. Agar xohlasangiz, hozir yangi to'plamni boshlashingiz mumkin."
        )
    elif user_id in users_loop and not users_loop[user_id]:
        await app.send_message(
            message.chat.id, 
            "To'plam jarayoni allaqachon to'xtatilgan. Bekor qilish uchun faol to‘plam yo‘q."
        )
    else:
        await app.send_message(
            message.chat.id, 
            "Bekor qilish uchun faol ommaviy fayllar yuklab olinmayapti."
    )
