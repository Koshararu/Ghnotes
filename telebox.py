# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: TeleboxUploader
# Description: Uploads files to Telebox service
# Author: ChatGPT
# Commands:
# .uploadtelebox
# ---------------------------------------------------------------------------------

import os
import requests
from .. import loader, utils

class TeleboxUploader(loader.Module):
    """Uploads files to Telebox service"""

    strings = {
        "name": "TeleboxUploader",
        "reply_to_file": "<b>Reply to a file to upload it to Telebox</b>",
        "uploading": "<b>Uploading to Telebox...</b>",
        "uploaded": "<b>File uploaded successfully: {}</b>",
        "upload_failed": "<b>Upload failed: {}</b>"
    }

    async def client_ready(self, client, db):
        self.client = client

    async def uploadteleboxcmd(self, message):
        """Uploads the replied file to Telebox"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings("reply_to_file", message))
            return
        
        file_path = await message.client.download_media(reply.media)
        await utils.answer(message, self.strings("uploading", message))

        try:
            with open(file_path, 'rb') as f:
                # Replace 'https://www.telebox.online/api/open/file_save' with the actual Telebox API endpoint
                # and 'JIlDLCrgtNwLoK3x' with your API key if required
                response = requests.post(
                    'https://telebox.com/api/upload',  # Hypothetical endpoint
                    files={'file': f},
                    headers={'Authorization': 'Bearer YOUR_API_KEY'}
                )

            if response.status_code == 200:
                data = response.json()
                file_url = data.get('url')  # Adjust based on the actual API response
                await utils.answer(message, self.strings("uploaded", message).format(file_url))
            else:
                await utils.answer(message, self.strings("upload_failed", message).format(response.text))
        except Exception as e:
            await utils.answer(message, self.strings("upload_failed", message).format(str(e)))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)