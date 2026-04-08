import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import moviepy.video.fx.all as vfx

def process_video_logic(input_path, output_path="result_tiktok.mp4"):
    # 1. Загружаем модель Whisper
    # 'base' — оптимально по скорости/качеству. 'tiny' — если будет тормозить.
    model = whisper.load_model("tiny")
    print("Распознаю речь...")
    result = model.transcribe(input_path, language="ru") # или "uk" для укр. выпуска
    
    video = VideoFileClip(input_path)
    
    # Для Тик-Тока лучше делать вертикальный формат 9:16
    # Обрезаем края, чтобы сделать видео вертикальным (center crop)
    w, h = video.size
    target_ratio = 9/16
    target_w = h * target_ratio
    video_vertical = video.crop(x_center=w/2, width=target_w)
    
    final_clips = []
    
    # 2. Обрабатываем сегменты речи
    # Берем первые 60 секунд, чтобы не выйти за лимиты памяти GitHub
    for segment in result['segments']:
        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()
        
        if start > 60: break # Ограничение для теста
        
        # Вырезаем кусочек видео
        clip = video_vertical.subclip(start, end)
        
        # ЭФФЕКТ: Плавное приближение (Зум)
        # Увеличиваем масштаб с 100% до 110% за время фразы
        clip = clip.resize(lambda t: 1 + 0.1 * (t / clip.duration))
        
        # ЭФФЕКТ: Субтитры
        txt_clip = TextClip(
            text, 
            fontsize=50, 
            color='yellow', 
            font='Arial-Bold',
            method='caption',
            size=(target_w*0.8, None) # Текст не шире 80% экрана
        ).set_start(0).set_duration(clip.duration).set_position(('center', h*0.7))
        
        # Накладываем текст на конкретный кусок
        combined = CompositeVideoClip([clip, txt_clip])
        final_clips.append(combined)
    
    # 3. Склеиваем всё в один ролик
    from moviepy.editor import concatenate_videoclips
    final_video = concatenate_videoclips(final_clips)
    
    # Сохраняем результат
    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    return output_path
