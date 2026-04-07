const ffmpeg = require('fluent-ffmpeg');

// Функция для поиска пауз и генерации команды нарезки
async function removeSilence(inputPath, outputPath) {
  return new Promise((resolve, reject) => {
    let silenceSegments = [];
    
    ffmpeg(inputPath)
      .audioFilters('silencedetect=n=-30dB:d=0.5') // Порог -30дБ, длительность от 0.5 сек
      .on('stderr', (line) => {
        // Парсим логи FFmpeg, чтобы найти моменты тишины
        if (line.includes('silence_start')) {
          const start = line.match(/silence_start: (\d+\.?\d*)/)[1];
          silenceSegments.push({ start: parseFloat(start) });
        }
        if (line.includes('silence_end')) {
          const end = line.match(/silence_end: (\d+\.?\d*)/)[1];
          silenceSegments[silenceSegments.length - 1].end = parseFloat(end);
        }
      })
      .on('end', () => {
        // После анализа запускаем вторую стадию — склейку фрагментов без тишины
        // Здесь обычно генерируется сложный фильтр 'select' для FFmpeg
        console.log("Silence detected at:", silenceSegments);
        resolve(silenceSegments);
      })
      .save('/dev/null'); // Только анализ, файл не создаем
  });
}
