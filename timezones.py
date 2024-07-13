from .. import loader, utils
import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder

class Timezones(loader.Module):
    """Модуль для вывода времени в определенном часовом поясе"""

    strings = {"name": "Timezones"}

    async def client_ready(self, client, db):
        self.db = db
        self._city = self.db.get(self.strings["name"], "city", "UTC")
        self._timezone = self.get_timezone_by_city(self._city)

    def get_timezone_by_city(self, city):
        tf = TimezoneFinder()
        timezone = None

        # Примерный список городов и их координат
        city_coordinates = {
            "Комсомольск-на-Амуре": (50.5495, 137.0075),
            "Москва": (55.7558, 37.6176),
            "Нью-Йорк": (40.7128, -74.0060),
            "Лондон": (51.5074, -0.1278),
            "Токио": (35.682839, 139.759455)
            # Добавьте другие города и их координаты по мере необходимости
        }

        coordinates = city_coordinates.get(city)
        if coordinates:
            latitude, longitude = coordinates
            timezone = tf.timezone_at(lat=latitude, lng=longitude)
        return timezone or "UTC"

    async def cfgcmd(self, message):
        """.cfg <город> - Установить часовой пояс по городу"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Пожалуйста, укажите город. Например: .cfg Москва")
            return

        timezone = self.get_timezone_by_city(args)
        if timezone == "UTC":
            await utils.answer(message, "Некорректный город или город не найден. Пожалуйста, используйте корректное название города.")
            return

        self._city = args
        self._timezone = timezone
        self.db.set(self.strings["name"], "city", self._city)
        self.db.set(self.strings["name"], "timezone", self._timezone)
        await utils.answer(message, f"Часовой пояс для города {self._city} установлен на {self._timezone}")

    async def tzcmd(self, message):
        """Выводит текущее время в установленном часовом поясе"""
        timezone = pytz.timezone(self._timezone)
        current_time = datetime.now(timezone)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        await utils.answer(message, f"Текущее время в {self._city} ({self._timezone}): {formatted_time}")