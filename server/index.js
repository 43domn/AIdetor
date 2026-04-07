const express = require('express');
const { generateLocalSubtitles } = require('./services/localWhisper');
const router = express.Router();

router.post('/api/ai/subtitles', async (req, res) => {
    // В реальности имя файла будет приходить от multer (загрузчика файлов)
    const { filename } = req.body; 

    if (!filename) {
        return res.status(400).json({ error: "No video file provided" });
    }

    try {
        const result = await generateLocalSubtitles(filename);
        
        // Возвращаем результат на фронтенд
        res.json({
            message: "Subtitles generated successfully",
            data: result.text,
            // Можно прочитать готовый SRT и отправить его текстом
            srtContent: require('fs').readFileSync(result.file, 'utf8') 
        });

    } catch (error) {
        res.status(500).json({ error: "AI Processing Failed" });
    }
});

module.exports = router;
