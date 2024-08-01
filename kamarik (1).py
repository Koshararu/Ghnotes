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

class kamar(loader.Module):
    """"""

    strings = {"name": "kamar"}

    async def kamarikcmd(self, message):
        """Аўта камарік раз в 4 гадзіны"""
        self.set("kamarik", True)
        while self.get("kamarik"):
            await message.reply("камар")
            await asyncio.sleep(14400)
        await message.delete()

    async def kamarcmd(self, message):
        """Аўта камар раз в 3 гадзіны"""
        self.set("kamar", True)
        while self.get("kamar"):
            await message.reply("Комару")
            await asyncio.sleep(10800)
        await message.delete()

    async def watcher(self, message):
        if not getattr(message, "out", False):
            return

        if message.raw_text.lower() == "комару стоп":
            self.set("kamarik", False)
            await utils.answer(message, "<b>Фарм комаріков остановлен.</b>")
            await message.delete()
        if message.raw_text.lower() == "камар стоп":
            self.set("kamar", False)
            await utils.answer(message, "<b>Фарм комару остановлен.</b>")
            await message.delete()
        if message.raw_text.lower() in [".kamarik", ".kamar"]:
            await message.delete()