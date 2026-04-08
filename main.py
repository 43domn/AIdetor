import os
import asyncio
import feedparser
import yt_dlp
from telegram import Bot
from dotenv import load_dotenv
from processor import process_video_logic

# Загружаем переменные из .env (если файл есть, для локального запуска)
load_dotenv()

# Настройки из секретов GitHub или .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# RSS фид канала "Орел и Решка"
RSS_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UC7O0_77v8-DIn_vO_fVvS_A"

def get_latest_video_url(rss_url):
    """Получает ссылку на последнее видео из RSS-ленты."""
    print("--- Проверяю YouTube канал ---")
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        return None
    return feed.entries[0].link

def download_video(url):
    """Скачивает видео. Настроено на низкое качество для экономии памяти GitHub."""
    print(f"--- Начинаю скачивание: {url} ---")
    output_filename = "input_video.mp4"
    
    # Если старый файл остался — удаляем
    if os.path.exists(output_filename):
        os.remove(output_filename)

    ydl_opts = {
        # Качаем 360p или 480p, чтобы сервер GitHub не завис
        'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'outtmpl': output_filename,
        # Ограничиваем скачивание первыми 2 минутами для теста
        'download_ranges': lambda info_dict, ydl: [{'start_time': 0, 'end_time': 120}],
        'force_keyframes_at_cuts': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return output_filename

async def send_to_telegram(file_path):
    """Отправляет готовый ролик в Telegram."""
    print("--- Отправляю результат в Telegram ---")
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Ошибка: Токены Telegram не найдены!")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    with open(file_path, 'rb') as video_file:
        await bot.send_video(
            chat_id=TELEGRAM_CHAT_ID, 
            video=video_file, 
            caption="Новый выпуск 'Орла и Решки' готов для TikTok! 🚀"
        )

async def main():
    try:
        # 1. Проверяем свежее видео
        video_url = get_latest_video_url(RSS_FEED_URL)
        if not video_url:
            print("Не удалось получить видео из RSS.")
            return

        # 2. Скачиваем
        raw_video_path = download_video(video_url)

        # 3. Обрабатываем через нейронки (вызываем твой processor.py)
        print("--- Запускаю ИИ-обработку (зум и субтитры) ---")
        processed_video_path = process_video_logic(raw_video_path)

        # 4. Отправляем в телегу
        await send_to_telegram(processed_video_path)
        
        print("--- Готово! Проверяй Telegram ---")

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
