from pyrogram import filters
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import subscribe
import asyncio
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf
# ------------------- Start-Buttons ------------------- #

from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
# Set bot commands in one place
@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("Siz ushbu buyruqdan foydalanish huquqiga ega emassiz.")
        return
    # Setting all the bot commands
    await app.set_bot_commands([
        BotCommand("start", "🚀 Botni ishga tushirish"),
        BotCommand("kirish", "🔑 Akkauntingizga kirish"),
        BotCommand("chiqish", "🚪 Akkauntingizdan chiqish"),
        BotCommand("ommaviy", "🫠 Ommaviy yuklab olish"), 
        BotCommand("bekor", "🚫 Jarayonni bekor qilish"),
        BotCommand("token", "🎲 3 soat cheklovsiz foydalanish"),
        BotCommand("sovga", "💘 Premium sovg'a qilish"),
        BotCommand("rejam", "⌛ Ta'rifingiz haqida ma'lumot"),
        BotCommand("sozlamalar", "⚙️ Sozmalar sahifasi"),
        BotCommand("stats", "📊 Bot statistikasi"),
        BotCommand("rejalar", "🗓️ Premium rejalar haqida"),
        BotCommand("shartlar", "🥺 Foydalanish shartlari"),
        BotCommand("speedtest", "🚅 Server tezligini o'lchash"),
        BotCommand("get", "🗄️ Barcha foydalanuvchilar IDsini olish"),
        BotCommand("qulflash", "🔒 Kanalingizni saqlab olishdan himoyalash"),
        BotCommand("broadcast", "⚡ Foydalanuvchilarga xabar yuborish"),
        BotCommand("yordam", "❓ Yordam kerak bo'lsa!"),
        BotCommand("dl", "💀 30+ saytlardan video yuklab olish"),
        BotCommand("adl", "👻 30+ saytlardan audio yuklab olish")
        
    ])
    
    await message.reply("✅ Buyruqlar muvaffaqqiyatli o'zgartiirildi!")

# Function to split and manage the help message in multiple parts

# Function to split and manage the help message in multiple parts
help_pages = [
    (
        "📝 **Bot buyruqlari haqida umumiy ma'lumot (1/2)**:\n\n"
        "1. **/add userID**\n"
        "> Foydalanuvchini premiumga qo‘shish (Faqat admin!)\n\n"
        "2. **/rem userID**\n"
        "> Foydalanuvchini premiumdan olib tashlash (Faqat admin!)\n\n"
        "3. **/sovga userID**\n"
        "> Premiumingizni do'stingizga sovg'a qilish uchun. (Faqat Premiumlar)\n\n"
        "4. **/get**\n"
        "> Barcha foydalanuvchilar IDsini olish (Faqat admin!)\n\n"
        "5. **/qulflash**\n"
        "> Kanaldan yuklashni cheklash (Faqat admin!)\n\n"
        "6. **/dl link**\n"
        "> Instagramdan video yuklab olish\n\n"
        "7. **/adl link**\n"
        "> Internetdan audio yuklab olish\n\n"
        "8. **/kirish**\n"
        "> Akkauntingizga kirish\n\n"
        "9. **/chiqish**\n"
        "> Akkauntingizdan chiqish\n\n"
    ),
    (
        "📝 **Bot buyruqlari haqida umumiy ma'lumot (2/2)**:\n\n"
        "10. **/ommaviy**\n"
        "> Bir vaqtda ketma ket postlarni yuklab olish (max 30 limit))\n\n"
        "11. **/stats**\n"
        "> Bot statistikasi\n\n"
        "12. **/rejalar**\n"
        "> Premium rejalar\n\n"
        "13. **/speedtest**\n"
        "> Server tezligini sinab ko'rish\n\n"
        "14. **/shartlar**\n"
        "> Foydalanish shartlari\n\n"
        "15. **/bekor**\n"
        "> Davom etayotgan ommaviy jarayonni bekor qiling\n\n"
        "16. **/rejam**\n"
        "> Ta'rif rejangiz haqida\n\n"
        "17. **/session**\n"
        "> Pyrogram V@ sessiya yaratish\n\n"
        "18. **/sozlama**\n"
        "> 1. CHATIDO'RNAT : To'g'ridan-to'g'ri kanalga yoki guruhga yoki foydalanuvchining dm-ga yuklash uchun -100[chatID] bilan foydalaning.\n"
        "> 2. QAYTANOMO'RNAT : Kanallaringiz nomini o'zgartirish yorlig'i yoki foydalanuvchi nomini qo'shish uchun\n"
        "> 3. SARLAVHA : Maxsus sarlavha qo'shish uchun\n"
        "> 4. SO'ZALMASHTIR :O'chirilgan to'plamdagi so'zlar uchun ishlatilishi mumkin\n"
        "> 5. QAYTATIKLA : Sozlamalarni asl holatiga qaytarish uchun\n\n"
        "> Siz sozlamalardan MAXSUS eskizi, SESSION asosidagi login va hokazolarni o‘rnatishingiz mumkin.\n\n"
        "**__Powered by @jonathanfrky__**"
    )
]

# Helper function to send or edit help messages with navigation buttons
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return

    # Define the navigation buttons (previous, next)
    prev_button = InlineKeyboardButton("◀️ Oldingi", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Keyingi ▶️", callback_data=f"help_next_{page_number}")

    # Add buttons conditionally
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)

    # Create the keyboard
    keyboard = InlineKeyboardMarkup([buttons])

    # Delete the previous message before sending a new one
    await message.delete()

    # Send the appropriate help page
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )

# Start command with help navigation
@app.on_message(filters.command("yordam"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
    
    # Show the first help page
    await send_or_edit_help_page(client, message, 0)

# Handle callback queries for help navigation
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])

    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1

    # Edit the appropriate help page
    await send_or_edit_help_page(client, callback_query.message, page_number)

    # Acknowledge the callback query
    await callback_query.answer()


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command("shartlar") & filters.private)
async def terms(client, message):
    terms_text = (
        "📜 **Foydalanish shartlari** 📜\n\n"
        "✨ Biz foydalanuvchi xatti-harakatlari uchun javobgar emasmiz va mualliflik huquqi bilan himoyalangan kontentni targ'ib qilmaymiz. Agar biron bir foydalanuvchi bunday faoliyat bilan shug'ullansa, bu faqat o'zining javobgarligidir.\n"
        "✨ Sotib olgach, biz ish vaqti, ishlamay qolish vaqti yoki rejaning amal qilishiga kafolat bermaymiz. __Foydalanuvchilarni avtorizatsiya qilish va taqiqlash bizning ixtiyorimizda; biz istalgan vaqtda foydalanuvchilarni taqiqlash yoki ruxsat berish huquqini saqlab qolamiz.__\n"
 )
    # Buttons for "See Plans" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 Ta'riflar ko'rish", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Bog'lanish", url="https://t.me/jonathanfrky")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)


@app.on_message(filters.command("rejalar") & filters.private)
async def plan(client, message):
    plan_text = (
        "💰 **Premium narx**: Hozircha bepul, Zavqlaning)\n"
        "📥 **Yuklab olish chegarasi**: Foydalanuvchilar bitta paketli buyruqda 100 000 tagacha faylni yuklab olishlari mumkin.\n"
        "🛑 **To'plam**: Siz ikkita rejimga ega bo'lasiz /ommaviy va /toplam.\n"
        " - Foydalanuvchilarga har qanday yuklab olish yoki yuklashni davom ettirishdan oldin jarayon avtomatik ravishda bekor qilinishini kutish tavsiya etiladi.\n\n"
        "📜 **Shartlar va shartlar**: Batafsil ma'lumot va to'liq shartlar uchun /shartlar ni yuboring.\n"
    )
    # Buttons for "See Terms" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 Shartlarni ko'rish", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Bog'lanish", url="https://t.me/jonathanfrky")],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "💰 **Premium narx**: Hozircha bepul, Zavqlaning)\n"
        "📥 **Yuklab olish chegarasi**: Foydalanuvchilar bitta paketli buyruqda 100 000 tagacha faylni yuklab olishlari mumkin.\n"
        "🛑 **To'plam**: Siz ikkita rejimga ega bo'lasiz /ommaviy va /toplam.\n"
        " - Foydalanuvchilarga har qanday yuklab olish yoki yuklashni davom ettirishdan oldin jarayon avtomatik ravishda bekor qilinishini kutish tavsiya etiladi.\n\n"
        "📜 **Shartlar va shartlar**: Batafsil ma'lumot va to'liq shartlar uchun /shartlar ni yuboring.\n"
    )
    # Buttons for "See Terms" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 Shartlarni ko'rish", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Bog'lanish", url="https://t.me/jonathanfrky")],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "📜 **Foydalanish shartlari** 📜\n\n"
        "✨ Biz foydalanuvchi xatti-harakatlari uchun javobgar emasmiz va mualliflik huquqi bilan himoyalangan kontentni targ'ib qilmaymiz. Agar biron bir foydalanuvchi bunday faoliyat bilan shug'ullansa, bu faqat o'zining javobgarligidir.\n"
        "✨ Sotib olgach, biz ish vaqti, ishlamay qolish vaqti yoki rejaning amal qilishiga kafolat bermaymiz. __Foydalanuvchilarni avtorizatsiya qilish va taqiqlash bizning ixtiyorimizda; biz istalgan vaqtda foydalanuvchilarni taqiqlash yoki ruxsat berish huquqini saqlab qolamiz.__\n"
 )
    # Buttons for "See Plans" and "Contact"
    buttons = InlineKeyboardMarkup(
        [
           [InlineKeyboardButton("📜 Shartlarni ko'rish", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Bog'lanish", url="https://t.me/jonathanfrky")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
    
