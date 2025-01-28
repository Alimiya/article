const { Telegraf } = require('telegraf');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// Telegram Bot API key
const TELEGRAM_API_KEY = '7633821666:AAEWv1ePzKOaXZ7W7kpYc6qmh7sAnHGnYko';
// Gemini API key
const GEMINI_API_KEY = 'AIzaSyCZQ-h6Gdkiw9B3G50kPRnNQSzOwVFj2Rs';

const bot = new Telegraf(TELEGRAM_API_KEY);

// State management
let userState = {};

bot.start((ctx) => {
  ctx.reply('Привет! Используйте /analyze, чтобы начать анализ записи.');
});

bot.command('analyze', (ctx) => {
  userState[ctx.chat.id] = { stage: 'SELECT_FORMAT' };
  ctx.reply('Выберите формат анализа:', {
    reply_markup: {
      keyboard: [["format1"]],
      one_time_keyboard: true,
      resize_keyboard: true,
    },
  });
});

bot.on('text', async (ctx) => {
  const chatId = ctx.chat.id;
  const state = userState[chatId];

  if (state && state.stage === 'SELECT_FORMAT') {
    userState[chatId].format = ctx.message.text;
    userState[chatId].stage = 'UPLOAD_AUDIO';
    ctx.reply('Отправьте вашу запись в формате wav.');
  } else {
    ctx.reply('Неизвестная команда. Пожалуйста, начните с команды /analyze.');
  }
});

bot.on('document', async (ctx) => {
  const chatId = ctx.chat.id;
  const state = userState[chatId];

  if (state && state.stage === 'UPLOAD_AUDIO') {
    console.log(fileId)
    const fileId = ctx.message.voice.file_id;
    const filePath = `./${fileId}.wav`;
    const fileLink = await ctx.telegram.getFileLink(fileId);

    const response = await fetch(fileLink);
    const buffer = await response.arrayBuffer();
    fs.writeFileSync(filePath, Buffer.from(buffer));

    ctx.reply('Обрабатываю запись...');

    try {
      // Call Python script to transcribe audio using Whisper
      const pythonScript = path.join(__dirname, 'transcribe.py');
      exec(`python3 ${pythonScript} ${filePath}`, (error, stdout, stderr) => {
        if (error) {
          console.error(`Ошибка при выполнении Python-скрипта: ${error.message}`);
          ctx.reply('Произошла ошибка при транскрипции записи. Попробуйте снова.');
          return;
        }

        if (stderr) {
          console.error(`Stderr: ${stderr}`);
        }

        const transcription = stdout.trim();
        ctx.reply(`Транскрипция завершена: \n${transcription}`);

        // Load format1 criteria from file
        const formatFilePath = path.join(__dirname, 'format1.txt');
        const formatCriteria = fs.readFileSync(formatFilePath, 'utf-8');

        const geminiPrompt = `Дай оценку с помощью этого критерия (${state.format}):\n${formatCriteria}\n\nТекст: ${transcription}`;

        // Call Gemini API for analysis
        const aiResponse = { data: { choices: [{ text: 'Пример анализа текста.' }] } }; // Mock response, replace with actual API call
        ctx.reply(`Анализ текста: \n${aiResponse.data.choices[0].text}`);

        // Cleanup
        fs.unlinkSync(filePath);
      });
    } catch (err) {
      console.error(err);
      ctx.reply('Произошла ошибка при обработке записи. Попробуйте снова.');
    }
  } else {
    ctx.reply('Пожалуйста, начните с команды /analyze и следуйте инструкциям.');
  }
});

bot.launch().then(() => console.log('Bot is running...')).catch(console.error);
