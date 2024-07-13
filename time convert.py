from .. import loader, utils

class TimeConverterMod(loader.Module):
    """Конвертирует время из одного формата в другой"""

    strings = {"name": "TimeConverterMod"}

    async def ctcmd(self, message):
        """.ct <time> - Конвертировать время (например, 10m, 1440m, 2h)"""

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Пожалуйста, предоставьте значение для конвертации (например, 10m, 1440m, 2h).")
            return

        unit = args[-1].lower()
        try:
            value = int(args[:-1])
        except ValueError:
            await utils.answer(message, "Некорректное значение. Используйте числовое значение и единицу времени (например, 10m, 1440m, 2h).")
            return

        if unit == 's':
            seconds = value
            minutes = value / 60
            hours = value / 3600
            days = value / 86400
        elif unit == 'm':
            seconds = value * 60
            minutes = value
            hours = value / 60
            days = value / 1440
        elif unit == 'h':
            seconds = value * 3600
            minutes = value * 60
            hours = value
            days = value / 24
        elif unit == 'd':
            seconds = value * 86400
            minutes = value * 1440
            hours = value * 24
            days = value
        else:
            await utils.answer(message, "Некорректная единица времени. Используйте 's' для секунд, 'm' для минут, 'h' для часов, 'd' для дней.")
            return

        response = (
            f"<b>Время конвертировано:</b>\n"
            f"<b>{seconds} секунд</b>\n"
            f"<b>{minutes:.2f} минут</b>\n"
            f"<b>{hours:.2f} часов</b>\n"
            f"<b>{days:.2f} дней</b>"
        )

        await utils.answer(message, response)