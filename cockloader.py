import imghdr
import io
import os
import random
import re

import requests
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class FileUploaderMod(loader.Module):
    """Different engines file uploader"""

    strings = {
        "name": "Uploader",
        "uploading": "🚀 <b>Uploading...</b>",
        "noargs": "🚫 <b>No file specified</b>",
        "err": "🚫 <b>Upload error</b>",
        "uploaded": '🎡 <b>File <a href="{0}">uploaded</a></b>!\n\n<code>{0}</code>',
        "not_an_image": "🚫 <b>This platform only supports images</b>",
    }

    strings_ru = {
        "uploading": "🚀 <b>Загрузка...</b>",
        "noargs": "🚫 <b>Файл не указан</b>",
        "err": "🚫 <b>Ошибка загрузки</b>",
        "uploaded": '🎡 <b>Файл <a href="{0}">загружен</a></b>!\n\n<code>{0}</code>',
        "not_an_image": "🚫 <b>Эта платформа поддерживает только изображения</b>",
        "_cmd_doc_oxo": "Загрузить на 0x0.st",
        "_cmd_doc_x0": "Загрузить на x0.at",
        "_cmd_doc_kappa": "Загрузить на kappa.lol",
        "_cls_doc": "Загружает файлы на различные хостинги",
    }

    async def get_media(self, message: Message):
        reply = await message.get_reply_message()
        m = None
        if reply and reply.media:
            m = reply
        elif message.media:
            m = message
        elif not reply:
            await utils.answer(message, self.strings("noargs"))
            return False

        if not m:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "file.txt"
        else:
            file = io.BytesIO(await self._client.download_media(m, bytes))
            file.name = (
                m.file.name
                or (
                    "".join(
                        [
                            random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
                            for _ in range(16)
                        ]
                    )
                )
                + m.file.ext
            )

        return file

    async def get_image(self, message: Message):
        file = await self.get_media(message)
        if not file:
            return False

        if imghdr.what(file) not in ["gif", "png", "jpg", "jpeg", "tiff", "bmp"]:
            await utils.answer(message, self.strings("not_an_image"))
            return False

        return file

    async def oxocmd(self, message: Message):
        """Upload to 0x0.st"""
        message = await utils.answer(message, self.strings("uploading"))
        file = await self.get_media(message)
        if not file:
            return

        try:
            oxo = await utils.run_sync(
                requests.post,
                "https://0x0.st",
                files={"file": file},
                data={"secret": True},
            )
        except ConnectionError:
            await utils.answer(message, self.strings("err"))
            return

        url = oxo.text
        await utils.answer(message, self.strings("uploaded").format(url))

    async def kappacmd(self, message: Message):
        """Upload to femboy beauty"""
        message = await utils.answer(message, self.strings("uploading"))
        file = await self.get_media(message)
        if not file:
            return

        try:
            kappa = await utils.run_sync(
                requests.post,
                "https://femboy.beauty/api/upload",
                files={"file": file},
            )
        except ConnectionError:
            await utils.answer(message, self.strings("err"))
            return

        url = f"https://femboy.beauty/{femboy.json()['id']}"
        await utils.answer(message, self.strings("uploaded").format(url))
