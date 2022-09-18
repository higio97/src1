#Anonim235

import os
from .. import bot as Drone
from telethon import events, Button

from ethon.mystarts import start_srb
    
S = '/' + 's' + 't' + 'a' + 'r' + 't'

@Drone.on(events.callbackquery.CallbackQuery(data="set"))
async def sett(event):    
    Drone = event.client                    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Kirimi Saya Gambar Apa Pun Untuk Thumbnail Sebagai `reply` Untuk Pesan ini.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("Media Tidak Ditemukan.")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("Media Tidak Ditemukan.")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Sedang Mencoba.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("Temporary thumbnail saved!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="rem"))
async def remt(event):  
    Drone = event.client            
    await event.edit('Sedang Mencoba.')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('Dihapus!')
    except Exception:
        await event.edit("Thumbnail Tidak Di Simpan.")                        
  
@Drone.on(events.NewMessage(incoming=True, pattern=f"{S}"))
async def start(event):
    text = "Kirimi Saya Tautan Pesan Apa Pun Untuk Mengkloningnya Di Sini, Untuk Pesan Channel Pribadi, Kirim Link Undangan Terlebih Dahulu.\n\n**SUPPORT:** @Anonim235"
    await start_srb(event, text)
    
