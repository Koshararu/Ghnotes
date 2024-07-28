# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: LayoutTranslator
# Description: Translates messages typed in the wrong keyboard layout (from English to Russian)
# Author: ChatGPT
# Commands:
# .translit
# ---------------------------------------------------------------------------------

from .. import loader, utils

class LayoutTranslator(loader.Module):
    """Translates messages typed in the wrong keyboard layout (from English to Russian)"""

    strings = {
        "name": "LayoutTranslator",
        "reply_to_message": "<b>Reply to a message to translate it</b>",
        "translating": "<b>Translating...</b>",
        "translated": "<b>Translated:</b> {}",
    }

    eng_to_rus = str.maketrans(
        "qwertyuiop[]asdfghjkl;'zxcvbnm,.",
        "йцукенгшщзхъфывапролджэячсмитьбю"
    )

    async def translitcmd(self, message):
        """Translates a message typed in the wrong keyboard layout (from English to Russian)"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("reply_to_message", message))
            return

        await utils.answer(message, self.strings("translating", message))

        original_text = reply.raw_text
        translated_text = original_text.translate(self.eng_to_rus)

        await utils.answer(message, self.strings("translated", message).format(translated_text))