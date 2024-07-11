# meta developer: 猫ちゃん

from .. import loader, utils
from telethon.tl.types import Message
import re
import asyncio

class Timer(loader.Module):
    """Timer"""

    strings = {
        "name": "Timer",
        "q": "<b>Current Timer for {}</b>\n<emoji document_id=5303396278179210513>👾</emoji> <i>{}:{}:{}</i> <b>left</b>"
    }

    async def pars(self, message, args, parsed):
        for i in args:
            if i[-1] not in ["h", "m", "s"]:
                args.remove(i)

        for i in args:
            parsed[i[-1]] = int(re.sub(r"[^a-zA-Z0-9]", "", i)[:-1])
        return parsed

    async def timercmd(self, message: Message):
        """ [5h 5m 5s] - turn on the timer"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, f"<b>Specify time</b>")
            return

        hours = 0
        mins = 0
        secs = 0
        parsed = {"h": None, "m": None, "s": None}
        args = args.split()
        r = await self.pars(message, args, parsed)
        if all(parsed[i] == None for i in parsed):
            await utils.answer(message, "<b>Time isn't specified</b>")
            return

        if r["h"]:
            hours = r["h"] * 3600
        if r["m"]:
            mins = r["m"] * 60
        if r["s"]:
            secs = r["s"]
        t = secs + mins + hours
        c = f"{t//3600}:{t%3600//60}:{t%3600%60}"

        while t > -1:
            h = f"{t//3600}"
            m = f"{t%3600//60}"
            s = f"{t%3600%60}"
            q = self.strings['q'].format(c, h, m, s)
            await utils.answer(message, q)
            t -= 1
            await asyncio.sleep(1)

        regex = r'\..*\<.*?\>.*'
        a = re.sub(regex, "\n<emoji document_id=5222108309795908493>✨</emoji> <b>Time's over</b>", q.replace("\n", "."))
        await utils.answer(message, a)
