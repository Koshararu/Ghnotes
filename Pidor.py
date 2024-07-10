from .. import loader, utils
import requests
import json
import re

def register(cb):
    cb(TTDownloadMod())

class TTDownloadMod(loader.Module):
    strings = {"name": "TTDownload"}

    async def client_ready(self, client, db):
        self.client = client

    async def ttdlcmd(self, message):
        if message.is_private:  # Проверяем, что сообщение из личной переписки
            reply = await message.get_reply_message()
            if reply:
                url = reply.raw_text
                if "tiktok.com" in url:
                    await message.edit("<b>Загрузка...</b>")
                    try:
                        r = requests.get(f"https://api.tiktok.com/get_video_info?url={url}")
                        data = r.json()
                        video_url = data["video_url"]
                        
                        video = requests.get(video_url).content
                        with open("video.mp4", "wb") as f:
                            f.write(video)
                        
                        await self.client.send_file(message.to_id, "video.mp4")
                        await message.delete()
                    except Exception as e:
                        await message.edit(f"<b>Ошибка: {e}</b>")
                else:
                    await message.edit("<b>Ответьте на сообщение с ссылкой на TikTok.</b>")
            else:
                await message.edit("<b>Ответьте на сообщение с ссылкой на TikTok.</b>")
