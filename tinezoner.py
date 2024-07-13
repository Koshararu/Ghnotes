import pytz
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinderL as TimezoneFinder
from telethon import types
from .. import loader, utils

class Timezones(loader.Module):
    """Модуль для отображения времени в заданной временной зоне"""

    strings = {"name": "Timezones"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.geolocator = Nominatim(user_agent="timezone_bot")
        self.tz_finder = TimezoneFinder()

    async def cityzcmd(self, message):
        """Используйте .cityz <город> чтобы задать город для временной зоны"""
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
            await utils.answer(message, "Город не задан. Используйте .cityz <город> чтобы задать город.")
            return

        try:
            # Поиск координат города
            location = self.geolocator.geocode(city)
            if not location:
                await utils.answer(message, "Не удалось найти город. Пожалуйста, укажите правильный город.")
                return

            # Получение часового пояса по координатам
            timezone_str = self.tz_finder.timezone_at(lng=location.longitude, lat=location.latitude)
            if not timezone_str:
                await utils.answer(message, "Не удалось определить часовой пояс для этого города.")
                return

            timezone = pytz.timezone(timezone_str)
        except Exception as e:
            await utils.answer(message, f"Произошла ошибка: {str(e)}")
            return

        # Получение текущего времени в заданном часовом поясе
        now = datetime.now(timezone)
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        await utils.answer(message, f"Текущее время в {city}: {current_time}")

# Пример конфигурации модуля
config = {
    "Timezones": {
        "city": "Комсомольск-на-Амуре"  # Задайте ваш город здесь
    }
}