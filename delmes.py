# ---------------------------------------------------------------------------------
#  /\_/\  🌐 Этот модуль был загружен через https://t.me/hikkamods_bot
# ( o.o )  🔓 Не лицензировано.
#  > ^ <   ⚠️ Владелец heta.hikariatama.ru не несет ответственности или прав интеллектуальной собственности на этот скрипт.
# ---------------------------------------------------------------------------------
# Name: DeleteMessages
# Description: Удаляет сообщения за определенный период времени и логирует количество удаленных сообщений.
# Author: BingChat
# ---------------------------------------------------------------------------------

from .. import loader, utils
import logging
from datetime import datetime, timedelta

class DeleteMessages(loader.Module):
    """Удаляет сообщения за определенный период времени и логирует количество удаленных сообщений."""

    strings = {"name": "DeleteMessages"}

    async def client_ready(self, client, db):
        self.client = client

    async def delmestcmd(self, message):
        """Используйте .delmest {X}{d/h/m} для удаления сообщений за определенный период времени."""
        args = utils.get_args_raw(message)
        if args:
            try:
                duration, unit = int(args[:-1]), args[-1]
                if unit == "d":
                    delta = timedelta(days=duration)
                elif unit == "h":
                    delta = timedelta(hours=duration)
                elif unit == "m":
                    delta = timedelta(minutes=duration)
                else:
                    await message.edit("Пожалуйста, используйте формат .delmest {X}{d/h/m}.")
                    return

                start_date = datetime.now() - delta
                count_deleted = 0
                async for msg in self.client.iter_messages(message.to_id, min_id=0, max_id=0, from_user="me"):
                    if msg.date.replace(tzinfo=None) > start_date:
                        await msg.delete()
                        count_deleted += 1
                
                logging.info(f"Удалено {count_deleted} сообщений за последние {duration} {unit}.")
                await message.edit(f"Удалено {count_deleted} сообщений за последние {duration} {unit}.")
            except ValueError:
                await message.edit("Пожалуйста, используйте формат .delmest {X}{d/h/m}.")
        else:
            await message.edit("Пожалуйста, укажите период времени для удаления сообщений.")

    async def delmescmd(self, message):
        """Используйте .delmes {X} / all для удаления сообщений."""
        args = utils.get_args_raw(message)
        if args:
            try:
                if args.lower() == "all":
                    async for msg in self.client.iter_messages(message.to_id, min_id=0, max_id=0, from_user="me"):
                        await msg.delete()
                    
                else:
                    count_deleted = 0
                    async for msg in self.client.iter_messages(message.to_id, min_id=0, max_id=0, from_user="me"):
                        if count_deleted >= int(args):
                            break
                        await msg.delete()
                        count_deleted += 1
                    
            except ValueError:
                await message.edit("Пожалуйста, используйте формат .delmes {X} или .delmes all.")
        else:
            await message.edit("Пожалуйста, укажите период времени для удаления сообщений.")
            
    async def delsocmd(self, message):
        """Используйте .delso {текст} для удаления ваших сообщений с определенным текстом."""
        args = utils.get_args_raw(message)
        if args:
            async for msg in self.client.iter_messages(message.to_id, search=args, from_user="me"):
                await msg.delete()
            await message.delete()
        else:
            await message.edit("Пожалуйста, укажите текст для поиска в ваших сообщениях.")