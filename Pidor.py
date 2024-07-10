import asyncio
import logging
import re
from telethon import events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from .. import loader, utils

class TTDownloadMod(loader.Module):
    """Скачать видео/фото/аудио из TikTok"""

    async def client_ready(self, client, db):
        self.db = db

    async def ttdcmd(self, message):
        """.ttd {link} - Скачать видео/фото/аудио из TikTok"""

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Пожалуйста, предоставьте ссылку на TikTok.")
            return

        await utils.answer(message, "Скачиваю...")

        chat = "@projectaltair_bot"
        bot_send_link = await message.client.send_message(chat, args)
        media_messages = []

        async def handler(event):
            if event.message.sender_id == (await message.client.get_peer_id(chat)) and event.message.media:
                logging.info("Получено медиа сообщение от бота")
                media_messages.append(event.message)

        # Добавляем обработчик событий
        message.client.add_event_handler(handler, events.NewMessage(incoming=True, from_users=chat))

        try:
            await asyncio.sleep(2)  # Ждем ответы от бота в течение 2 секунд после последнего сообщения
            if media_messages:
                photos = [msg.media for msg in media_messages if isinstance(msg.media, MessageMediaPhoto)]
                documents = [msg.media for msg in media_messages if isinstance(msg.media, MessageMediaDocument)]
                
                # Отправка фотографий
                if photos:
                    await message.client.send_file(message.to_id, photos, caption="По ссылке лень переходить было")

                # Отправка документов (видео/аудио)
                if documents:
                    for doc in documents:
                        await message.client.send_file(message.to_id, doc, caption="По ссылке лень переходить было")
        finally:
            # Удаляем обработчик событий и сообщения
            message.client.remove_event_handler(handler, events.NewMessage(incoming=True, from_users=chat))
            await bot_send_link.delete()
            await message.delete()

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
                "• " + "\n• ".join(["<code>" + str(i) + "</code>" for i in users_list]),
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
            if message.chat_id not in users:
                return

            links = re.findall(
                r"((?:https?://)?v[mt]\.tiktok\.com/[A-Za-z0-9_]+/?)", message.raw_text
            )

            if not links:
                return

            chat = "@projectaltair_bot"
            async with message.client.conversation(chat) as conv:
                for link in links:
                    await utils.answer(message, f"Отправляю ссылку в бот @projectaltair_bot: {link}")

                    bot_send_link = await conv.send_message(link)
                    media_messages = []

                    async def handler(event):
                        if event.message.sender_id == (await message.client.get_peer_id(chat)) and event.message.media:
                            logging.info("Получено медиа сообщение от бота")
                            media_messages.append(event.message)

                    # Добавляем обработчик событий
                    message.client.add_event_handler(handler, events.NewMessage(incoming=True, from_users=chat))

                    try:
                        await asyncio.sleep(2)  # Ждем ответы от бота в течение 2 секунд после последнего сообщения
                        if media_messages:
                            photos = [msg.media for msg in media_messages if isinstance(msg.media, MessageMediaPhoto)]
                            documents = [msg.media for msg in media_messages if isinstance(msg.media, MessageMediaDocument)]
                            
                            # Отправка фотографий
                            if photos:
                                await message.client.send_file(message.chat_id, photos, caption="По ссылке лень переходить было")

                            # Отправка документов (видео/аудио)
                            if documents:
                                for doc in documents:
                                    await message.client.send_file(message.chat_id, doc, caption="По ссылке лень переходить было")
                    finally:
                        # Удаляем обработчик событий и сообщения
                        message.client.remove_event_handler(handler, events.NewMessage(incoming=True, from_users=chat))
                        await bot_send_link.delete()

        except Exception as e:
            await utils.answer(message, f"Произошла ошибка: {str(e)}")
            
