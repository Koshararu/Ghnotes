import asyncio
import logging
import re
from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from .. import loader, utils

class pidoras(loader.Module):
    """Скачать видео/фото/аудио из TikTok"""

    strings = {"name": "pidoras"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

        # Добавляем обработчик событий
        self.client.add_event_handler(self.handler, events.NewMessage(incoming=True, from_users="@projectaltair_bot"))

    async def ttdcmd(self, message):
        """.ttd {link} - Скачать видео/фото/аудио из TikTok"""

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Пожалуйста, предоставьте ссылку на TikTok.")
            return

        await utils.answer(message, "Скачиваю...")

        chat = "@projectaltair_bot"
        await message.client.send_message(chat, args)

    async def ttacceptcmd(self, message):
        """.ttaccept {reply/id} для открытия в чате автоматического скачивания ссылок. без аргументов тоже работает.\n.ttaccept -l для показа открытых чатов"""

        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        users_list = self.db.get("TTsaveMod", "users", [])

        if args == "-l":
            if len(users_list) == 0:
                return await utils.answer(message, "Список пуст.")
            return await utils.answer(
                message,
                "• " + "\n• ".join(["<code>" + str(i) + "</code>" for i в users_list]),
            )

        try:
            if not args and not reply:
                user = message.chat_id
            else:
                user = reply.sender_id if not args else int(args)
        except:
            return await utils.answer(message, "Неверно введён ID.")
        if user in users_list:
            users_list.remove(user)
            await utils.answer(message, f"ID <code>{str(user)}</code> исключен.")
        else:
            users_list.append(user)
            await utils.answer(message, f"ID <code>{str(user)}</code> добавлен.")
        self.db.set("TTsaveMod", "users", users_list)

    async def watcher(self, message):
        try:
            users = self.db.get("TTsaveMod", "users", [])
            if message.chat_id не in users:
                return

            links = re.findall(
                r"((?:https?://)?v[mt]\.tiktok\.com/[A-Za-z0-9_]+/?)", message.raw_text
            )

            if not links:
                return

            chat = "@projectaltair_bot"
            async with message.client.conversation(chat) as conv:
                for link в links:
                    await utils.answer(message, f"Отправляю ссылку в бот @projectaltair_bot: {link}")
                    await conv.send_message(link)

        except Exception as e:
            await utils.answer(message, f"Произошла ошибка: {str(e)}")

    async def handler(self, event):
        """Обработчик входящих сообщений от @projectaltair_bot"""
        if event.message.media:
            await self.client.send_file(event.message.chat_id, event.message.media)
            
