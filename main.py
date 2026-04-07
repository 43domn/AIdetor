import os
import feedparser
import yt_dlp
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from telegram import Bot
import asyncio
from processor import process_video_logic


# 1. МОНИТОРИНГ RSS
def get_latest_video(rss_url):
    feed = feedparser.parse(rss_url)
    # Возвращает ссылку на последнее видео
    return feed.entries[0].link

# 2. СКАЧИВАНИЕ
def download_video(url):
    ydl_opts = {
        'format': 'best[height<=720]', # 720p хватит для Тик-Тока
        'outtmpl': 'input_video.mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "input_video.mp4"

# 3. ИИ-ОБРАБОТКА (Субтитры и монтаж)
def process_video(input_path):
    # Загружаем Whisper (модель base быстрая, но medium точнее)
    model = whisper.load_model("base")
    result = model.transcribe(input_path)
    
    video = VideoFileClip(input_path)
    
    # Пример "умного" зума: приближаем центр каждые 10 секунд для динамики
    # (Это упрощенный пример, в реальности можно искать паузы в речи)
    short_video = video.subclip(0, 60) # Берем первую минуту для теста
    
    # Добавляем субтитры (упрощенно)
    clips = [short_video]
    for segment in result['segments'][:10]: # Первые 10 фраз
        if segment['start'] < 60:
            txt = TextClip(segment['text'], fontsize=40, color='yellow', font='Arial-Bold')
            txt = txt.set_start(segment['start']).set_duration(segment['end']-segment['start']).set_pos('center')
            clips.append(txt)

    final = CompositeVideoClip(clips)
    final.write_videofile("result_tiktok.mp4", fps=30, codec="libx264")
    return "result_tiktok.mp4"

# 4. ОТПРАВКА В TELEGRAM
async def send_to_tg(file_path):
    bot = Bot(token="ТВОЙ_ТОКЕН_БОТА")
    await bot.send_video(chat_id="ТВОЙ_ID", video=open(file_path, 'rb'))

async def main():
    rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC7O0_77v8-DIn_vO_fVvS_A" # ID канала Орла и Решки
    print("Проверяю обновления...")
    video_url = get_latest_video(rss_url)
    
    print(f"Качаю: {video_url}")
    path = download_video(video_url)
    
    print("Нейронка обрабатывает видео...")
    final_path = process_video_logic(path)

    
    print("Отправляю в Telegram...")
    await send_to_tg(final_path)

if __name__ == "__main__":
    asyncio.run(main())
