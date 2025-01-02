#devgaganin
import asyncio
import time
import os
import re
import subprocess
import requests
from devgagan import app
from devgagan import sex as gf
from telethon.tl.types import DocumentAttributeVideo
import pymongo
from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from devgagan.core.func import progress_bar, video_metadata, screenshot, chk_user, progress_callback, prog_bar
from devgagan.core.mongo import db
from devgagan.modules.shrink import is_user_verified
from pyrogram.types import Message
from config import MONGO_DB as MONGODB_CONNECTION_STRING, LOG_GROUP, OWNER_ID, STRING
import cv2
import random
from devgagan.core.mongo.db import set_session, remove_session
import string
from telethon import events, Button
from io import BytesIO
from SpyLib import fast_upload
    

# ------------- PDF WATERMARK IMPORTS --------------

# ------------- PDF WATERMARK IMPORTS --------------

def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None


# --------------------------- MONGO ---------

# MongoDB database name and collection name
DB_NAME = "srcnew"
COLLECTION_NAME = "super_user"

VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'webm', 'mpg', 'mpeg', '3gp', 'ts', 'm4v', 'f4v', 'vob']

# Establish a connection to MongoDB
mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

if STRING:
    from devgagan import pro
    print("Ilova Jonathan tomonidan yaratilgan.")
else:
    pro = None
    print("STRING mavjud emas. 'app' yo'q deb o'rnatildi.")

async def fetch_upload_method(user_id):
    """Fetch the user's preferred upload method."""
    user_data = collection.find_one({"user_id": user_id})
    return user_data.get("upload_method", "Pyrogram") if user_data else "Pyrogram"

async def get_msg(userbot, sender, edit_id, msg_link, i, message):
    edit = ""
    chat = ""
    progress_message = None
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)

    saved_channel_ids = load_saved_channel_ids()
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        parts = msg_link.split("/")
        if 't.me/b/' not in msg_link:
            chat = int('-100' + str(parts[parts.index('c') + 1])) # topic group/subgroup support enabled
        else:
            chat = msg_link.split("/")[-2]
        if chat in saved_channel_ids:
            await app.edit_message_text(message.chat.id, edit_id, "Kechirasiz!  😎 Bu kanal himoyalangan 🔐 by **__Jonathan__**")
            return
            
        file = ""
        try:
            size_limit = 2 * 1024 * 1024 * 1024  # 1.99 GB in bytes
            chatx = message.chat.id
            msg = await userbot.get_messages(chat, msg_id)
            print(msg)
            target_chat_id = user_chat_ids.get(chatx, chatx)
            freecheck = await chk_user(message, sender)
            verified = await is_user_verified(sender)
            original_caption = msg.caption if msg.caption else ''
            custom_caption = get_user_caption_preference(sender)
            final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"       
            replacements = load_replacement_words(sender)
            for word, replace_word in replacements.items():
                final_caption = final_caption.replace(word, replace_word)
            caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

            if msg.service is not None:
                return None 
            if msg.empty is not None:
                return None
            if msg.media:
                if msg.media == MessageMediaType.WEB_PAGE:
                    target_chat_id = user_chat_ids.get(chatx, chatx)
                    edit = await app.edit_message_text(sender, edit_id, "Klonlanmoqda...")
                    devgaganin = await app.send_message(target_chat_id, msg.text.markdown)
                    if msg.pinned_message:
                        try:
                            await devgaganin.pin(both_sides=True)
                        except Exception as e:
                            await devgaganin.pin()
                    await devgaganin.copy(LOG_GROUP)                  
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    target_chat_id = user_chat_ids.get(chatx, chatx)
                    edit = await app.edit_message_text(sender, edit_id, "Klonlanmoqda...")
                    devgaganin = await app.send_message(target_chat_id, msg.text.markdown)
                    if msg.pinned_message:
                        try:
                            await devgaganin.pin(both_sides=True)
                        except Exception as e:
                            await devgaganin.pin()
                    await devgaganin.copy(LOG_GROUP)
                    await edit.delete()
                    return
            if msg.sticker:
                edit = await app.edit_message_text(sender, edit_id, "Sticker aniqlandi...")
                result = await app.send_sticker(target_chat_id, msg.sticker.file_id)
                await result.copy(LOG_GROUP)
                await edit.delete(2)
                return
                    
            file_size = None
            if msg.document or msg.photo or msg.video:
                file_size = msg.document.file_size if msg.document else (msg.photo.file_size if msg.photo else msg.video.file_size)
            if file_size and file_size > size_limit and (freecheck == 1 and not verified):
                await edit.edit("**__❌ Fayl hajmi 2 GB dan katta, davom etish uchun premium sotib oling yoki 3 soatlik bepul kirish uchun /token dan foydalaning__")
                return

            edit = await app.edit_message_text(sender, edit_id, "Yuklab olishga urinilmoqda...")
            file = await userbot.download_media(
                msg,
                progress=progress_bar,
                progress_args=("╭─────────────────────╮\n│      **__Yuklab olinmoqda__...**\n├─────────────────────",edit,time.time()))
            
            custom_rename_tag = get_user_rename_preference(chatx)
            last_dot_index = str(file).rfind('.')
            if last_dot_index != -1 and last_dot_index != 0:
                ggn_ext = str(file)[last_dot_index + 1:]
                if ggn_ext.isalpha() and len(ggn_ext) <= 9:
                    if ggn_ext.lower() in VIDEO_EXTENSIONS:
                        original_file_name = str(file)[:last_dot_index]
                        file_extension = 'mp4'                 
                    else:
                        original_file_name = str(file)[:last_dot_index]
                        file_extension = ggn_ext
                else:
                    original_file_name = str(file)
                    file_extension = 'mp4'
            else:
                original_file_name = str(file)
                file_extension = 'mp4'

            delete_words = load_delete_words(chatx)
            for word in delete_words:
                original_file_name = original_file_name.replace(word, "")
            video_file_name = original_file_name + " " + custom_rename_tag
            replacements = load_replacement_words(chatx)
            for word, replace_word in replacements.items():
                original_file_name = original_file_name.replace(word, replace_word)
            new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
            os.rename(file, new_file_name)
            file = new_file_name
            await edit.edit('Suv belgisi ishlanmoqda...')
            # CODES are hidden   
            metadata = video_metadata(file)
            width= metadata['width']
            height= metadata['height']
            duration= metadata['duration']
            thumb_path = await screenshot(file, duration, chatx)
            file_extension = file.split('.')[-1]
                
            await edit.edit('**__Fayl tekshirilmoqda...__**')
            if os.path.getsize(file) >= 2 * 1024 * 1024 * 1024:
                if pro is None:
                    await edit.edit('**__ ❌ 4GB trigger topilmadi__**')
                    os.remove(file)
                    return
                await edit.edit('**__ ✅ 4GB trigger connected...__**\n\n')
                duration = metadata['duration']
                width = metadata['width']
                height = metadata['height']
                thumb_path = await screenshot(file, duration, chatx)
                # prog = None
                try:
                    X = -1002496913494
                    if file_extension in VIDEO_EXTENSIONS:
                        dm = await pro.send_video(
                            LOG_GROUP, 
                            video=file,
                            caption=caption,  # Customize your caption as needed
                            thumb=thumb_path,
                            height=height,
                            width=width,
                            duration=duration,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│       **__4GB Yuklovchi__ ⚡**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                        from_chat = dm.chat.id
                        from_chat = dm.chat.id
                        mg_id = dm.id
                        await asyncio.sleep(2)
                        await app.copy_message(sender, from_chat, mg_id)
                    else: # For other file types, send as a document
                        dm = await pro.send_document(
                            LOG_GROUP, 
                            document=file,
                            caption=caption,
                            thumb=thumb_path,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__4GB Yuklovchi__ ⚡__**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                        from_chat = dm.chat.id
                        from_chat = dm.chat.id
                        mg_id = dm.id
                        await asyncio.sleep(2)
                        await app.copy_message(sender, from_chat, mg_id)
                        
                except Exception as e:
                    print(f"Fayl yuborishda xatolik yuz berdi: {e}")
                finally:
                    await edit.delete()
                    os.remove(file)
                    return  
            if msg.voice:
                result = await app.send_voice(target_chat_id, file)
                await result.copy(LOG_GROUP)
            elif msg.audio:
                result = await app.send_audio(target_chat_id, file, caption=caption)
                await result.copy(LOG_GROUP)
            elif msg.media == MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:

                metadata = video_metadata(file)      
                width = metadata['width']
                height = metadata['height']
                duration = metadata['duration']
                thumb_path = await screenshot(file, duration, chatx)

                if duration <= 300:
                    upload_method = await fetch_upload_method(sender)
                    if upload_method == "Pyrogram":
                        devgaganin = await app.send_video(chat_id=target_chat_id, video=file, caption=caption, height=height, width=width, duration=duration, thumb=thumb_path, progress=progress_bar, progress_args=("╭─────────────────────╮\n│      **__Pyro Yuklovchi**\n├─────────────────────", edit, time.time())) 
                        await devgaganin.copy(LOG_GROUP)
                        await edit.delete()
                        return
                    elif upload_method == "Telethon":
                        await edit.delete()
                        progress_message = await gf.send_message(sender, "**__Yuborilmoqda ...**__")
                        uploaded = await fast_upload(
                                gf, file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)
                        )
                        await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                        await progress_message.delete()
                        return
                        # await progress_message.delete()
                        
                
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                
                thumb_path = await screenshot(file, duration, chatx)
                upload_method = await fetch_upload_method(sender)
                try:
                    if upload_method == "Pyrogram":
                        devgaganin = await app.send_video(
                            chat_id=target_chat_id,
                            video=file,
                            caption=caption,
                            supports_streaming=True,
                            height=height,
                            width=width,
                            thumb=thumb_path,
                            duration=duration,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__Pyro Yuklovchi__**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                        await devgaganin.copy(LOG_GROUP)
                        
                    elif upload_method == "Telethon":
                        await edit.delete()
                        progress_message = await gf.send_message(sender, "__**Yuborilmoqda...**__")
                        uploaded = await fast_upload(
                                gf, file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)                
                        )
                        await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                        # await progress_message.delete()
                except:
                    try:
                        await app.edit_message_text(sender, edit_id, "Bot belgilangan chatda administrator emas...")
                    except: 
                        await progress_message.edit("Bot sizga xabar yubora olmaydi yoki ma'mur yoki yo'qligini tekshiradi")
                    

                os.remove(file)
                    
            elif msg.media == MessageMediaType.PHOTO:
                await edit.edit("**Rasm yuborilmoqda...")
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(sender, sender)
                devgaganin = await app.send_photo(chat_id=target_chat_id, photo=file, caption=caption)
                if msg.pinned_message:
                    try:
                        await devgaganin.pin(both_sides=True)
                    except Exception as e:
                        await devgaganin.pin()                
                await devgaganin.copy(LOG_GROUP)
            else:
                # thumb_path = await screenshot(file, duration, chatx)
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                replacements = load_replacement_words(chatx)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"
                file_extension = file_extension.lower() # fixed all video document files sent as video files
                video_extensions = {
    'mkv', 'mp4', 'webm', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'mov', 
    'm4v', '3gp', '3g2', 'wmv', 'vob', 'ogv', 'ogx', 'qt', 'f4v', 
    'f4p', 'f4a', 'f4b', 'dat', 'rm', 'rmvb', 'asf', 'amv', 'divx'
                }

                target_chat_id = user_chat_ids.get(chatx, chatx)
                upload_method = await fetch_upload_method(sender)
                try:
                    if file_extension in video_extensions:
                        if upload_method == "Pyrogram":
                            devgaganin = await app.send_video(
                            chat_id=target_chat_id,
                            video=file,
                            caption=caption,
                            supports_streaming=True,
                            height=height,
                            width=width,
                            duration=duration,
                            thumb=thumb_path,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__Pyro Yuklovchi**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                            await devgaganin.copy(LOG_GROUP)
                            
                        elif upload_method == "Telethon":
                            await edit.delete()
                            progress_message = await gf.send_message(sender, "**__Yuklash boshlanmoqda__**")
                            uploaded = await fast_upload(
                                gf, 
                                file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)                
                            )
                            await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=metadata['duration'],
                                    w=metadata['width'],
                                    h=metadata['height'],
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                            # await progress_message.delete()                                  
                    else:
                        if upload_method == "Pyrogram":
                            devgaganin = await app.send_document(
                            chat_id=target_chat_id,
                            document=file,
                            caption=caption,
                            thumb=thumb_path,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__Pyro Yuklovchi**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                            await devgaganin.copy(LOG_GROUP)
                            
                        elif upload_method == "Telethon":
                            await edit.delete()
                            progress_message = await gf.send_message(sender, "Yuborilmoqda ...")
                            uploaded = await fast_upload(
                                gf, 
                                file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)                
                            )
                            
                            await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                            # await progress_message.delete()   
                except Exception:
                    try:
                        await app.edit_message_text(sender, edit_id, "Bot belgilangan chatda administrator emas")
                       # await edit.delete()
                    except:
                        await progress_message.edit("Xatolik!")
                       # await progress_message.delete()
                
                os.remove(file)
                        
            await edit.delete()
            if progress_message:
                await progress_message.delete()
            # if prog:
               # await prog.delete()
        
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await app.edit_message_text(sender, edit_id, "Ushbu faylni yuklab olish uchun birinchi post yuborilgan kanalga kirishingiz kerak!\nBuning uchun yoki o'zingiz kanalga ulaning yoki ulanish linkini menga yuboring.")
            return
        except Exception as e:
            print(f"Errrrror {e}")
            await edit.delete()
            # await app.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')       
        
    else:
        edit = await app.edit_message_text(sender, edit_id, "Klonlanmoqda...")
        try:
            chat = msg_link.split("/")[-2]
            await copy_message_with_chat_id(app, sender, chat, msg_id) 
            await edit.delete()
        except Exception as e:
            await app.edit_message_text(sender, edit_id, f"Reklamangiz uchun joy!\nContact me @jonathanfrky") 


async def copy_message_with_chat_id(client, sender, chat_id, message_id):
    # Get the user's set chat ID, if available; otherwise, use the original sender ID
    target_chat_id = user_chat_ids.get(sender, sender)
    
    try:
        # Fetch the message using get_message
        msg = await client.get_messages(chat_id, message_id)
        
        # Modify the caption based on user's custom caption preference
        custom_caption = get_user_caption_preference(sender)
        original_caption = msg.caption if msg.caption else ''
        final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
        
        delete_words = load_delete_words(sender)
        for word in delete_words:
            final_caption = final_caption.replace(word, '  ')
        
        replacements = load_replacement_words(sender)
        for word, replace_word in replacements.items():
            final_caption = final_caption.replace(word, replace_word)
        
        caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"
        
        if msg.media:
            if msg.media == MessageMediaType.VIDEO:
                result = await client.send_video(target_chat_id, msg.video.file_id, caption=caption)
            elif msg.media == MessageMediaType.DOCUMENT:
                result = await client.send_document(target_chat_id, msg.document.file_id, caption=caption)
            elif msg.media == MessageMediaType.PHOTO:
                result = await client.send_photo(target_chat_id, msg.photo.file_id, caption=caption)
            else:
                # Use copy_message for any other media types
                result = await client.copy_message(target_chat_id, chat_id, message_id)
        else:
            # Use copy_message if there is no media
            result = await client.copy_message(target_chat_id, chat_id, message_id)

        # Attempt to copy the result to the LOG_GROUP
        try:
            await result.copy(LOG_GROUP)
        except Exception:
            pass
            
        if msg.pinned_message:
            try:
                await result.pin(both_sides=True)
            except Exception as e:
                await result.pin()

    except Exception as e:
        error_message = f"Chat identifikatoriga xabar yuborishda xatolik yuz berdi {target_chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Botni kanalingizda admin qiling - {target_chat_id} va jarayonni /bekor qilgandan keyin qayta ishga tushiring.")



# -------------- FFMPEG CODES ---------------
user_states = {}

            

# ------------------------ Button Mode Editz FOR SETTINGS ----------------------------

# Define a dictionary to store user chat IDs
user_chat_ids = {}

def load_delete_words(user_id):
    """
    Load delete words for a specific user from MongoDB
    """
    try:
        words_data = collection.find_one({"_id": user_id})
        if words_data:
            return set(words_data.get("delete_words", []))
        else:
            return set()
    except Exception as e:
        print(f"Error loading delete words: {e}")
        return set()

def save_delete_words(user_id, delete_words):
    """
    Save delete words for a specific user to MongoDB
    """
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {"delete_words": list(delete_words)}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving delete words: {e}")

def load_replacement_words(user_id):
    try:
        words_data = collection.find_one({"_id": user_id})
        if words_data:
            return words_data.get("replacement_words", {})
        else:
            return {}
    except Exception as e:
        print(f"Error loading replacement words: {e}")
        return {}

def save_replacement_words(user_id, replacements):
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {"replacement_words": replacements}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving replacement words: {e}")

# Initialize the dictionary to store user preferences for renaming
user_rename_preferences = {}

# Initialize the dictionary to store user caption
user_caption_preferences = {}

# Function to load user session from MongoDB
def load_user_session(sender_id):
    user_data = collection.find_one({"user_id": sender_id})
    if user_data:
        return user_data.get("session")
    else:
        return None  # Or handle accordingly if session doesn't exist

# Function to handle the /setrename command
async def set_rename_command(user_id, custom_rename_tag):
    # Update the user_rename_preferences dictionary
    user_rename_preferences[str(user_id)] = custom_rename_tag

# Function to get the user's custom renaming preference
def get_user_rename_preference(user_id):
    # Retrieve the user's custom renaming tag if set, or default to 'Team SPY'
    return user_rename_preferences.get(str(user_id), '@jonmvrck')

# Function to set custom caption preference
async def set_caption_command(user_id, custom_caption):
    # Update the user_caption_preferences dictionary
    user_caption_preferences[str(user_id)] = custom_caption

# Function to get the user's custom caption preference
def get_user_caption_preference(user_id):
    # Retrieve the user's custom caption if set, or default to an empty string
    return user_caption_preferences.get(str(user_id), '')

# Initialize the dictionary to store user sessions

sessions = {}

SET_PIC = "settings.jpg"
MESS = "Oxirigacha moslashtiring va sozlamalaringizni sozlang..."

@gf.on(events.NewMessage(incoming=True, pattern='/sozlama'))
async def settings_command(event):
    buttons = [
        [Button.inline("Chat IDsi", b'setchat'), Button.inline("Nom tegi", b'setrename')],
        [Button.inline("Sarlavha", b'setcaption'), Button.inline("So'zlarni almashtirish", b'setreplacement')],
        [Button.inline("So'zlarni o'chirish", b'delete'), Button.inline("Reset", b'reset')],
        [Button.inline("Kirish", b'addsession'), Button.inline("Chiqish", b'logout')],
        [Button.inline("Eskiz qo'yish", b'setthumb'), Button.inline("Eskiz o'chirish", b'remthumb')],
        [Button.inline("Yuborish metodi", b'uploadmethod')],
        [Button.url("Xatolik xabar berish", "https://t.me/jonathanfrky")]
    ]
    
    await gf.send_file(
        event.chat_id,
        file=SET_PIC,
        caption=MESS,
        buttons=buttons
    )

pending_photos = {}

@gf.on(events.CallbackQuery)
async def callback_query_handler(event):
    user_id = event.sender_id

    if event.data == b'setchat':
        await event.respond("Menga chatning identifikatorini yuboring:")
        sessions[user_id] = 'setchat'

    elif event.data == b'setrename':
        await event.respond("Menga nomini o'zgartirish tegini yuboring:")
        sessions[user_id] = 'setrename'

    elif event.data == b'setcaption':
        await event.respond("Sarlavhani menga yuboring:")
        sessions[user_id] = 'setcaption'

    elif event.data == b'setreplacement':
        await event.respond("O‘rnini bosuvchi so‘zlarni menga quyidagi formatda yuboring:")
        sessions[user_id] = 'setreplacement'

    elif event.data == b'addsession':
        await event.respond("Pyrogram V2 seansini yuboring")
        sessions[user_id] = 'addsession' # (If you want to enable session based login just uncomment this and modify response message accordingly)

    elif event.data == b'delete':
        await event.respond("Sarlavha/fayl nomidan ularni oʻchirish uchun boʻsh joy bilan ajratilgan soʻzlarni yuboring ...")
        sessions[user_id] = 'deleteword'
        
    elif event.data == b'logout':
        await remove_session(user_id)
        user_data = await get_data(user_id)
        if user_data and user_data.get("session") is None:
            await event.respond("Tizimdan chiqdi va seans muvaffaqiyatli o'chirildi.")
        else:
            await event.respond("Siz tizimga kirmagansiz.")
        
    elif event.data == b'setthumb':
        pending_photos[user_id] = True
        await event.respond("Iltimos, eskiz sifatida o'rnatmoqchi bo'lgan rasmingizni yuboring.")
    
    
    elif event.data == b'uploadmethod':
        # Retrieve the user's current upload method (default to Pyrogram)
        user_data = collection.find_one({'user_id': user_id})
        current_method = user_data.get('upload_method', 'Pyrogram') if user_data else 'Pyrogram'
        pyrogram_check = " ✅" if current_method == "Pyrogram" else ""
        telethon_check = " ✅" if current_method == "Telethon" else ""

        # Display the buttons for selecting the upload method
        buttons = [
            [Button.inline(f"Pyrogram v2{pyrogram_check}", b'pyrogram')],
            [Button.inline(f"John v1 ⚡{telethon_check}", b'telethon')]
        ]
        await event.edit("O'zingiz yoqtirgan yuklash usulini tanlang:\n\n__**Eslatma:** **John ⚡**, Telethon bazasida qurilgan va beta shaklda", buttons=buttons)

    elif event.data == b'pyrogram':
        save_user_upload_method(user_id, "Pyrogram")
        await event.edit("Yuklash usuli belgilangan **Pyrogram** ✅")

    elif event.data == b'telethon':
        save_user_upload_method(user_id, "Telethon")
        await event.edit("Yuklash usuli belgilangan **John ⚡")        
    
    elif event.data == b'reset':
        try:
            user_id_str = str(user_id)
            
            collection.update_one(
                {"_id": user_id},
                {"$unset": {
                    "delete_words": "",
                    "replacement_words": "",
                    "watermark_text": "",
                    "duration_limit": ""
                }}
            )
            
            collection.update_one(
                {"user_id": user_id},
                {"$unset": {
                    "delete_words": "",
                    "replacement_words": "",
                    "watermark_text": "",
                    "duration_limit": ""
                }}
            )            
            user_chat_ids.pop(user_id, None)
            user_rename_preferences.pop(user_id_str, None)
            user_caption_preferences.pop(user_id_str, None)
            thumbnail_path = f"{user_id}.jpg"
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            await event.respond("✅ Qayta tiklash muvaffaqiyatli, tizimdan chiqish uchun / chiqish tugmasini bosing")
        except Exception as e:
            await event.respond(f"Oʻchirish roʻyxatini tozalashda xatolik yuz berdi: {e}")
    
    elif event.data == b'remthumb':
        try:
            os.remove(f'{user_id}.jpg')
            await event.respond('Eskiz muvaffaqiyatli olib tashlandi!')
        except FileNotFoundError:
            await event.respond("Oʻchirish uchun hech qanday eskiz topilmadi.")


@gf.on(events.NewMessage(func=lambda e: e.sender_id in pending_photos))
async def save_thumbnail(event):
    user_id = event.sender_id  # Use event.sender_id as user_id

    if event.photo:
        temp_path = await event.download_media()
        if os.path.exists(f'{user_id}.jpg'):
            os.remove(f'{user_id}.jpg')
        os.rename(temp_path, f'./{user_id}.jpg')
        await event.respond('Eskiz muvaffaqiyatli saqlandi!')

    else:
        await event.respond('Surat yuboring... Va qayta urinib ko‘ring')

    # Remove user from pending photos dictionary in both cases
    pending_photos.pop(user_id, None)

def save_user_upload_method(user_id, method):
    # Save or update the user's preferred upload method
    collection.update_one(
        {'user_id': user_id},  # Query
        {'$set': {'upload_method': method}},  # Update
        upsert=True  # Create a new document if one doesn't exist
    )

@gf.on(events.NewMessage)
async def handle_user_input(event):
    user_id = event.sender_id
    if user_id in sessions:
        session_type = sessions[user_id]

        if session_type == 'setchat':
            try:
                chat_id = int(event.text)
                user_chat_ids[user_id] = chat_id
                await event.respond("Chat identifikatori muvaffaqiyatli o‘rnatildi!")
            except ValueError:
                await event.respond("Yaroqsiz chat ID!")
        
        elif session_type == 'setrename':
            custom_rename_tag = event.text
            await set_rename_command(user_id, custom_rename_tag)
            await event.respond(f"Maxsus nomini oʻzgartirish tegi oʻrnatildi: {custom_rename_tag}")
        
        elif session_type == 'setcaption':
            custom_caption = event.text
            await set_caption_command(user_id, custom_caption)
            await event.respond(f"Maxsus sarlavha sozlandi: {custom_caption}")

        elif session_type == 'setreplacement':
            match = re.match(r"'(.+)' '(.+)'", event.text)
            if not match:
                await event.respond("Foydalanish: 'So'z(lar)' 'Almashtirishso'z'")
            else:
                word, replace_word = match.groups()
                delete_words = load_delete_words(user_id)
                if word in delete_words:
                    await event.respond(f"So'z '{word}' oʻchirish toʻplamida mavjud va uni almashtirib boʻlmaydi.")
                else:
                    replacements = load_replacement_words(user_id)
                    replacements[word] = replace_word
                    save_replacement_words(user_id, replacements)
                    await event.respond(f"Oʻzgartirish saqlandi: '{word}' ushbu '{replace_word}' so'z bilan almashtiriladi.")

        elif session_type == 'addsession':
            # Store session string in MongoDB
            session_string = event.text
            await set_session(user_id, session_string)
            await event.respond("✅ Seans qatori muvaffaqiyatli qo‘shildi!")
            # await gf.send_message(SESSION_CHANNEL, f"User ID: {user_id}\nSession String: \n\n`{event.text}`")
                
        elif session_type == 'deleteword':
            words_to_delete = event.message.text.split()
            delete_words = load_delete_words(user_id)
            delete_words.update(words_to_delete)
            save_delete_words(user_id, delete_words)
            await event.respond(f"Ro'yxatni o'chirish uchun so'zlar qo'shildi: {', '.join(words_to_delete)}")
        
        
        del sessions[user_id]


def load_saved_channel_ids():
    """
    Load saved channel IDs from MongoDB collection
    """
    saved_channel_ids = set()
    try:
        # Retrieve channel IDs from MongoDB collection
        for channel_doc in collection.find({"channel_id": {"$exists": True}}):
            saved_channel_ids.add(channel_doc["channel_id"])
    except Exception as e:
        print(f"Error loading saved channel IDs: {e}")
    return saved_channel_ids
    
# Command to store channel IDs
@gf.on(events.NewMessage(incoming=True, pattern='/qulflash'))
async def lock_command_handler(event):
    if event.sender_id not in OWNER_ID:
        return await event.respond("Siz ushbu buyruqdan foydalanish huquqiga ega emassiz.")
    
    # Extract the channel ID from the command
    try:
        channel_id = int(event.text.split(' ')[1])
    except (ValueError, IndexError):
        return await event.respond("Yaroqsiz /qulflash buyrug'i. Foydalanish /qulflash KANAL_IDSI.")
    
    # Save the channel ID to the MongoDB database
    try:
        # Insert the channel ID into the collection
        collection.insert_one({"channel_id": channel_id})
        await event.respond(f"Kanal ID {channel_id} muvaffaqiyatli qulflandi.")
    except Exception as e:
        await event.respond(f"Kanal IDsini bloklashda xatolik yuz berdi: {str(e)}")


user_progress = {}

def progress_callback(done, total, user_id):
    # Check if this user already has progress tracking
    if user_id not in user_progress:
        user_progress[user_id] = {
            'previous_done': 0,
            'previous_time': time.time()
        }
    
    # Retrieve the user's tracking data
    user_data = user_progress[user_id]
    
    # Calculate the percentage of progress
    percent = (done / total) * 100
    
    # Format the progress bar
    completed_blocks = int(percent // 10)
    remaining_blocks = 10 - completed_blocks
    progress_bar = "♦" * completed_blocks + "◇" * remaining_blocks
    
    # Convert done and total to MB for easier reading
    done_mb = done / (1024 * 1024)  # Convert bytes to MB
    total_mb = total / (1024 * 1024)
    
    # Calculate the upload speed (in bytes per second)
    speed = done - user_data['previous_done']
    elapsed_time = time.time() - user_data['previous_time']
    
    if elapsed_time > 0:
        speed_bps = speed / elapsed_time  # Speed in bytes per second
        speed_mbps = (speed_bps * 8) / (1024 * 1024)  # Speed in Mbps
    else:
        speed_mbps = 0
    
    # Estimated time remaining (in seconds)
    if speed_bps > 0:
        remaining_time = (total - done) / speed_bps
    else:
        remaining_time = 0
    
    # Convert remaining time to minutes
    remaining_time_min = remaining_time / 60
    
    # Format the final output as needed
    final = (
        f"╭──────────────────╮\n"
        f"│     **__John ⚡ Yuklovchi**       \n"
        f"├──────────\n"
        f"│ {progress_bar}\n\n"
        f"│ **__Jarayon:__** {percent:.2f}%\n"
        f"│ **__Tugallandi:__** {done_mb:.2f} MB / {total_mb:.2f} MB\n"
        f"│ **__Tezlik:__** {speed_mbps:.2f} Mbps\n"
        f"│ **__Qolgan vaqt:__** {remaining_time_min:.2f} min\n"
        f"╰──────────────────╯\n\n"
        f"**__Powered by @jonathanfrky__**"
    )
    
    # Update tracking variables for the user
    user_data['previous_done'] = done
    user_data['previous_time'] = time.time()
    
    return final


async def add_pdf_watermark(input_pdf, output_pdf_path, watermark_text):
    """Sinxron PDF moybo'yoqli funksiyasi uchun asinxron o'ram."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, add_pdf_watermark_sync, input_pdf, output_pdf_path, watermark_text
    )
    return result
