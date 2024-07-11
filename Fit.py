import re
import requests
from telethon import TelegramClient, events

# Настройки Telegram
api_id = '24299459'
api_hash = 'bff996fd15bd2ceef62c2813ac9f6fb2'
bot_token = '7388896120:AAE7oC2mo99QUMThMDE_bPEE1h-lHdSGV5s'

# Настройки логгера
logging.basicConfig(level=logging.INFO)

# Создание клиента Telegram
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)


# Функция для извлечения ссылки на видео без вотермарки
def get_video_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': url,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Ищем прямую ссылку на видео без вотермарки в HTML-коде страницы
        match = re.search(r'videoObject\.url":"([^"]+)"', response.text)
        if match:
            video_url = match.group(1)
            return video_url
    return None


# Обработчик всех сообщений
@client.on(events.NewMessage())
async def all_messages_handler(event):
    # Проверяем, содержит ли сообщение ссылку на TikTok
    message = event.message
    urls = message.entities
    
    if not urls:
        return
    
    for entity in urls:
        if entity.type == 'url':
            url = entity.url
            
            if 'tiktok.com' in url:
                # Пытаемся извлечь ссылку на видео без вотермарки
                video_url = get_video_url(url)
                if video_url:
                    # Отправляем видео пользователю
                    await client.send_message(message.to_id, video_url)
                    await message.delete()  # Удаляем сообщение с ссылкой
                else:
                    await message.reply("Не удалось найти видео без вотермарки.")


async def main():
    await client.run_until_disconnected()


if name == 'main':
    asyncio.run(main())
