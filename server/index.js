const express = require('express');
const ffmpeg = require('fluent-ffmpeg');
const path = require('path');

const app = express();

app.post('/api/edit', (req, res) => {
    const { inputFile, startTime, duration } = req.body;

    ffmpeg(path.join(__dirname, 'uploads', inputFile))
        .setStartTime(startTime)
        .setDuration(duration)
        .withVideoCodec('libx264') // Профессиональный кодек
        .withAudioCodec('aac')
        .on('end', () => {
            res.json({ message: 'Editing complete', file: 'output.mp4' });
        })
        .on('error', (err) => {
            res.status(500).json({ error: err.message });
        })
        .save(path.join(__dirname, 'processed', 'output.mp4'));
});

app.listen(5000, () => console.log('AI Video Processor running on port 5000'));
