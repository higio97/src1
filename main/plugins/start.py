#Anonim235

import os
from .. import bot
from telethon import events, Button, TelegramClient

from pyrogram import idle
from main.plugins.main import Bot, userbot

st = "Kirim Saya Tautan Pesan Untuk Mengkloningnya Di Sini, Untuk Channel Pribadi, Kirim Link Undangan Terlebih Dahulu.\n\n**SUPPORT:** @Anonim235\n**DEV:** @Anonim235"

@bot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(f'{st}', 
                      buttons=[
                              [Button.inline("SET THUMB.", data="sett"),
                               Button.inline("REM THUMB.", data="remt")]
                              ])
    try:
        await Bot.start()
        await userbot.start()
        await idle()
    except Exception as e:
        if 'Client is already connected' in str(e):
            pass
        else:
            await event.client.send_message(event.chat_id, "Error while starting Client, check if your API and SESSION is right.")
            return
    
@bot.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Kirim Saya Gambar Apapun Untuk Thumbnail Dengan Cara `reply` Pesan Nya.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("Media Tidak Di Temukan.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("Gambar Tidak Di Temukan")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Sedang Mencoba.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("Thumbnail Temporer Disimpan!")
        
@bot.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    Drone = event.client            
    await event.edit('Sedang Mencoba.')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('Dihapus!')
    except Exception:
        await event.edit("Tidak Ada Thumbnail Temporer Disimpan!")                        
    
    
