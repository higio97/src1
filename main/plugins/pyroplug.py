# Anonim235

import asyncio, time, os

from .. import Bot, bot
from main.plugins.progress import progress_for_pyrogram
from main.plugins.helpers import screenshot

from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid
from ethon.pyfunc import video_metadata
from telethon import events

def thumbnail(sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    else:
         return None
      
async def check(userbot, client, link):
    msg_id = int(link.split("/")[-1])
    if 't.me/c/' in link:
        try:
            chat = int('-100' + str(link.split("/")[-2]))
            await userbot.get_messages(chat, msg_id)
            return True, None
        except ValueError:
            return False, "**Link Tidak Valid!**"
        except Exception:
            return False, "Sudahkah Kamu Bergabung Pada Channel?"
    else:
        try:
            chat = str(link.split("/")[-2])
            await client.get_messages(chat, msg_id)
            return True, None
        except Exception:
            return False, "Mungkin Bot Diblokir Dari Obrolan, atau Link Kamu Tidak Valid!"
            
async def get_msg(userbot, client, sender, edit_id, msg_link, i):
    edit = ""
    chat = ""
    msg_id = int(msg_link.split("/")[-1]) + int(i)
    if 't.me/c/' in msg_link:
        chat = int('-100' + str(msg_link.split("/")[-2]))
        try:
            msg = await userbot.get_messages(chat, msg_id)
            if msg.media:
                if 'web_page' in msg.media:
                    edit = await client.edit_message_text(sender, edit_id, "Kloning.")
                    await client.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    edit = await client.edit_message_text(sender, edit_id, "Kloning.")
                    await client.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            edit = await client.edit_message_text(sender, edit_id, "Mencoba Mengunduh.")
            file = await userbot.download_media(
                msg,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    "**MENGUNDUH:**\n",
                    edit,
                    time.time()
                )
            )
            await edit.edit('Bersiap Untuk Mengunggah!')
            caption = str(file)
            if msg.caption is not None:
                caption = msg.caption
            if str(file).split(".")[-1] in ['mkv', 'mp4', 'webm']:
                if str(file).split(".")[-1] in ['webm', 'mkv']:
                    path = str(file).split(".")[0] + ".mp4"
                    os.rename(file, path) 
                    file = str(file).split(".")[0] + ".mp4"
                data = video_metadata(file)
                duration = data["duration"]
                thumb_path = await screenshot(file, duration, sender)
                await client.send_video(
                    chat_id=sender,
                    video=file,
                    caption=caption,
                    supports_streaming=True,
                    duration=duration,
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**MENGUNGGAH:**\n',
                        edit,
                        time.time()
                    )
                )
            elif str(file).split(".")[-1] in ['jpg', 'jpeg', 'png', 'webp']:
                await edit.edit("Mengunggah Foto.")
                await bot.send_file(sender, file, caption=caption)
            else:
                thumb_path=thumbnail(sender)
                await client.send_document(
                    sender,
                    file, 
                    caption=caption,
                    thumb=thumb_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        client,
                        '**MENGUNGGAH:**\n',
                        edit,
                        time.time()
                    )
                )
            await edit.delete()
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await client.edit_message_text(sender, edit_id, "Sudahkah Kamu Bergabung Pada Channel?")
            return 
        except Exception as e:
            await client.edit_message_text(sender, edit_id, f'Gagal Menyimpan: `{msg_link}`')
            return 
    else:
        edit = await client.edit_message_text(sender, edit_id, "Kloning.")
        chat =  msg_link.split("/")[-2]
        try:
            await client.copy_message(int(sender), chat, msg_id)
        except Exception as e:
            print(e)
            return await client.edit_message_text(sender, edit_id, f'Gagal Menyimpan: `{msg_link}`')
        await edit.delete()
        
async def get_bulk_msg(userbot, client, sender, msg_link, i):
    x = await client.send_message(sender, "Sedang Proses!")
    await get_msg(userbot, client, sender, x.message_id, msg_link, i) 
