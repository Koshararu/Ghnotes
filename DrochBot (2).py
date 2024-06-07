__version__ = (1, 0, 0)
#
#
# _           _            _ _
# | |         | |          (_) |
# | |     ___ | |_ ___  ___ _| | __
# | |    / _ \| __/ _ \/ __| | |/ /
# | |___| (_) | || (_) \__ \ |   <
# \_____/\___/ \__\___/|___/_|_|\_\
#
#              © Copyright 2022
#
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikkaftgmods
# meta banner: https://i.imgur.com/awltLuz.jpeg


from .. import loader, utils
import asyncio

class DrochBotMod(loader.Module):
    """"""

    strings = {"name": "ADB"}

    async def drochcmd(self, message):
        """Автодроч"""
        self.set("droch", True)
        while self.get("droch"):
            await message.reply("Подрочить")
            await asyncio.sleep(600)
        await message.delete()

    async def dickcmd(self, message):
        """Автохуй"""
        self.set("dick", True)
        while self.get("dick"):
            await message.reply("/dick")
            await asyncio.sleep(3600)
        await message.delete()

    async def watcher(self, message):
        if not getattr(message, "out", False):
            return

        if message.raw_text.lower() == "дрочка стоп":
            self.set("droch", False)
            await utils.answer(message, "<b>Дрочка остановлена.</b>")
            await message.delete()
        if message.raw_text.lower() == "хуй стоп":
            self.set("dick", False)
            await utils.answer(message, "<b>Рост хуя остановлен.</b>")
            await message.delete()
        if message.raw_text.lower() in [".dick", ".droch"]:
            await message.delete()
