const ffmpeg = require('fluent-ffmpeg');
const whisper = require('whisper-node');
const path = require('path');
const fs = require('fs');

// Шаг 1: Конвертация видео в нужный аудиоформат (WAV, 16kHz, Mono)
const extractAudioForAI = (videoPath, outputPath) => {
    return new Promise((resolve, reject) => {
        ffmpeg(videoPath)
            .toFormat('wav')
            .audioChannels(1) // Моно
            .audioFrequency(16000) // Требование Whisper
            .on('end', () => resolve(outputPath))
            .on('error', (err) => reject(err))
            .save(outputPath);
    });
};

// Шаг 2: Запуск локальной нейросети
const generateLocalSubtitles = async (videoFilename) => {
    const videoPath = path.join(__dirname, '../../uploads', videoFilename);
    const audioPath = path.join(__dirname, '../../uploads', `temp_${Date.now()}.wav`);

    console.log('🟡 [NEXUS AI] Извлечение аудио...');
    await extractAudioForAI(videoPath, audioPath);

    console.log('🟡 [NEXUS AI] Запуск нейросети (Whisper Local)...');
    
    // Настройки локальной модели
    const options = {
        modelName: "base", // 'tiny', 'base', 'small', 'medium'. Base - лучший баланс скорости и качества.
        whisperOptions: {
            language: "auto", // Автоопределение языка (или 'ru', 'en')
            gen_file_txt: false,
            gen_file_subtitle: true, // Автоматически создаст .srt файл
            gen_file_vtt: false,
            word_timestamps: false // Поставь true, если захочешь караоке-эффект
        }
    };

    try {
        // Транскрибация файла
        const transcript = await whisper.whisper(audioPath, options);
        
        // Удаляем временный аудиофайл, чтобы не забивать сервер
        fs.unlinkSync(audioPath);

        console.log('🟢 [NEXUS AI] Субтитры готовы!');
        
        // whisper-node создает файл с тем же именем, но расширением .srt
        const srtPath = audioPath + '.srt'; 
        return { success: true, text: transcript, file: srtPath };

    } catch (error) {
        console.error('🔴 [NEXUS AI] Ошибка генерации:', error);
        if (fs.existsSync(audioPath)) fs.unlinkSync(audioPath);
        throw error;
    }
};

module.exports = { generateLocalSubtitles };
