import pytz
from datetime import datetime
from telethon import types
from .. import loader, utils

class Timezones(loader.Module):
    """Модуль для отображения времени в заданной временной зоне"""

    strings = {"name": "Timezones"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def cfgcmd(self, message):
        """Используйте .cfg <город> чтобы задать город для временной зоны"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Пожалуйста, укажите город.")
            return

        self.db.set("Timezones", "city", args)
        await utils.answer(message, f"Город для временной зоны установлен на {args}.")

    async def tzcmd(self, message):
        """Используйте .tz чтобы показать текущее время в заданной временной зоне"""
        city = self.db.get("Timezones", "city", None)
        if not city:
            await utils.answer(message, "Город не задан. Используйте .cfg <город> чтобы задать город.")
            return

        try:
            # Получение часового пояса по названию города
            timezone = pytz.timezone(city)
        except pytz.UnknownTimeZoneError:
            await utils.answer(message, "Неизвестный город. Пожалуйста, укажите правильный город.")
            return

        # Получение текущего времени в заданном часовом поясе
        now = datetime.now(timezone)
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        await utils.answer(message, f"Текущее время в {city}: {current_time}")

# Пример конфигурации модуля
config = {
    "Timezones": {
        "city": "Europe/Moscow"  # Задайте ваш город здесь
    }
}