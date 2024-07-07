import imghdr
import io
import os
import random
@@ -20,19 +19,14 @@ class FileUploaderMod(loader.Module):
        "uploading": "🚀 <b>Uploading...</b>",
        "noargs": "🚫 <b>No file specified</b>",
        "err": "🚫 <b>Upload error</b>",
        "uploaded": '🎡 <b>File <a href="{0}">uploaded</a></b>!\n\n<code>{0}</code>',
        "imgur_blocked": "🚫 <b>Unban @ImgUploadBot</b>",
        "not_an_image": "🚫 <b>This platform only supports images</b>",
        "uploaded": '🎡 <b>File <a href="{0}">uploaded</a></b>!\n\n<code>{0}</code
    }

    strings_ru = {
        "uploading": "🚀 <b>Загрузка...</b>",
        "noargs": "🚫 <b>Файл не указан</b>",
        "err": "🚫 <b>Ошибка загрузки</b>",
        "uploaded": '🎡 <b>Файл <a href="{0}">загружен</a></b>!\n\n<code>{0}</code>',
        "imgur_blocked": "🚫 <b>Разблокируй @ImgUploadBot</b>",
        "not_an_image": "🚫 <b>Эта платформа поддерживает только изображения</b>",
        "_cmd_doc_imgur": "Загрузить на imgur.com",
        "uploaded": '🎡 <b>Файл <a href="{0}">загружен</a></b>!\n\n<code>{0}</code
        "_cmd_doc_oxo": "Загрузить на 0x0.st",
        "_cmd_doc_x0": "Загрузить на x0.at",
        "_cmd_doc_skynet": "Загрузить на децентрализованную платформу SkyNet",
@@ -71,17 +65,6 @@ async def get_media(self, message: Message):

        return file

    async def get_image(self, message: Message):
        file = await self.get_media(message)
        if not file:
            return False

        if imghdr.what(file) not in ["gif", "png", "jpg", "jpeg", "tiff", "bmp"]:
            await utils.answer(message, self.strings("not_an_image"))
            return False

        return file

    async def skynetcmd(self, message: Message):
        """Upload to decentralized SkyNet"""
        message = await utils.answer(message, self.strings("uploading"))
@@ -106,42 +89,7 @@ async def skynetcmd(self, message: Message):
            ),
        )

    async def imgurcmd(self, message: Message):
        """Upload to imgur.com"""
        message = await utils.answer(message, self.strings("uploading"))
        file = await self.get_image(message)
        if not file:
            return

        chat = "@ImgUploadBot"

        async with self._client.conversation(chat) as conv:
            try:
                m = await conv.send_message(file=file)
                response = await conv.get_response()
            except YouBlockedUserError:
                await utils.answer(message, self.strings("imgur_blocked"))
                return

            await m.delete()
            await response.delete()

            try:
                url = (
                    re.search(
                        r'<meta property="og:image" data-react-helmet="true"'
                        r' content="(.*?)"',
                        (await utils.run_sync(requests.get, response.raw_text)).text,
                    )
                    .group(1)
                    .split("?")[0]
                )
            except Exception:
                url = response.raw_text

            await utils.answer(message, self.strings("uploaded").format(url))

    async def oxocmd(self, message: Message):
async def oxocmd(self, message: Message):
        """Upload to 0x0.st"""
        message = await utils.answer(message, self.strings("uploading"))
        file = await self.get_media(message)
