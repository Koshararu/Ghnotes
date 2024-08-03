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
                                await message.client.send_file(message.chat_id, photos, caption="")

                            # Отправка документов (видео/аудио)
                            if documents:
                                for doc in documents:
                                    await message.client.send_file(message.chat_id, doc, caption="")
                    finally:
                        # Удаляем обработчик событий и сообщения
                        message.client.remove_event_handler(handler, events.NewMessage(incoming=True, from_users=chat))                      

        except Exception as e:
            await utils.answer(message, f"Произошла ошибка: {str(e)}")