from .. import loader, utils

class LayoutTranslator(loader.Module):
    """Translates messages typed in the wrong keyboard layout (from English to Russian and vice versa)"""

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

    rus_to_eng = str.maketrans(
        "йцукенгшщзхъфывапролджэячсмитьбю",
        "qwertyuiop[]asdfghjkl;'zxcvbnm,."
    )

    def _text_frequency(self, text):
        """Calculate the frequency of letters in the text"""
        frequency = {}
        for char in text.lower():
            if char.isalpha():
                frequency[char] = frequency.get(char, 0) + 1
        return frequency

    def _is_likely_english(self, text):
        """Check if the text is likely to be in English based on letter frequency"""
        frequency = self._text_frequency(text)
        # Check if the frequency of English letters is higher than Russian letters
        english_letters = set("qwertyuiopasdfghjklzxcvbnm")
        russian_letters = set("йцукенгшщзхъфывапролджэячсмитьбю")

        english_count = sum(frequency.get(letter, 0) for letter in english_letters)
        russian_count = sum(frequency.get(letter, 0) for letter in russian_letters)

        return english_count > russian_count

    async def translitcmd(self, message):
        """Translates a message typed in the wrong keyboard layout"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("reply_to_message", message))
            return

        await utils.answer(message, self.strings("translating", message))

        original_text = reply.raw_text

        # Determine the translation direction based on letter frequency
        if self._is_likely_english(original_text):
            translated_text = original_text.translate(self.eng_to_rus)
        else:
            translated_text = original_text.translate(self.rus_to_eng)

        await utils.answer(message, self.strings("translated", message).format(translated_text))