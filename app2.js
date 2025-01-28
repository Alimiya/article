const { Telegraf } = require('telegraf');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch'); // Для работы с fetch в Node.js

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
    ctx.reply('Отправьте вашу запись');
  } else {
    ctx.reply('Неизвестная команда. Пожалуйста, начните с команды /analyze.');
  }
});

// Обрабатываем отправку аудио-файла
bot.on('document', async (ctx) => {
console.log('Документ получен', ctx.message.document)
  const chatId = ctx.chat.id;
  const state = userState[chatId];
  ctx.reply('good')
  if (state && state.stage === 'UPLOAD_AUDIO') {
    ctx.reply('double good')
    const file = ctx.message.document;
    const fileId = file.file_id;
    const fileName = file.file_name;
    
    const fileLink = await ctx.telegram.getFileLink(fileId);
    const fileExtension = path.extname(fileName).toLowerCase();

    // Загружаем файл
    try {
      const response = await fetch(fileLink);
      const buffer = await response.buffer();
      const filePath = path.join(__dirname, `${fileId}${fileExtension}`);
      fs.writeFileSync(filePath, buffer);

      ctx.reply('Обрабатываю запись...');

      // Если файл в формате ogg, конвертируем в wav
      const convertedFilePath = path.join(__dirname, `${fileId}.wav`);
      if (fileExtension !== '.wav') {
        exec(`ffmpeg -i ${filePath} ${convertedFilePath}`, (error, stdout, stderr) => {
          if (error) {
            console.error(`Ошибка при конвертации файла: ${error.message}`);
            ctx.reply('Произошла ошибка при обработке записи. Попробуйте снова.');
            return;
          }

          if (stderr) {
            console.error(`Stderr: ${stderr}`);
          }

          // Теперь вызываем Python-скрипт для транскрипции
          const pythonScript = path.join(__dirname, 'transcribe.py');
          exec(`python3 ${pythonScript} ${convertedFilePath}`, (error, stdout, stderr) => {
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

            // Загрузить форматные критерии
            const formatFilePath = path.join(__dirname, 'format1.txt');
            const formatCriteria = fs.readFileSync(formatFilePath, 'utf-8');

            const geminiPrompt = `Дай оценку с помощью этого критерия (${state.format}):\n${formatCriteria}\n\nТекст: ${transcription}`;

            // Имитация ответа от Gemini API
            const aiResponse = { data: { choices: [{ text: 'Пример анализа текста.' }] } }; // Замените на настоящий запрос к API
            ctx.reply(`Анализ текста: \n${aiResponse.data.choices[0].text}`);

            // Удалить временные файлы
            fs.unlinkSync(filePath);
            fs.unlinkSync(convertedFilePath);
          });
        });
      } else {
        // Если файл уже в нужном формате, сразу обрабатываем
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

          // Загрузить форматные критерии
          const formatFilePath = path.join(__dirname, 'format1.txt');
          const formatCriteria = fs.readFileSync(formatFilePath, 'utf-8');

          const geminiPrompt = `Дай оценку с помощью этого критерия (${state.format}):\n${formatCriteria}\n\nТекст: ${transcription}`;

          // Имитация ответа от Gemini API
          const aiResponse = { data: { choices: [{ text: 'Пример анализа текста.' }] } }; // Замените на настоящий запрос к API
          ctx.reply(`Анализ текста: \n${aiResponse.data.choices[0].text}`);

          // Удалить временные файлы
          fs.unlinkSync(filePath);
        });
      }
    } catch (err) {
      console.error('Ошибка при загрузке файла:', err);
      ctx.reply('Произошла ошибка при загрузке записи. Попробуйте снова.');
    }
  } else {
    ctx.reply('Пожалуйста, начните с команды /analyze и следуйте инструкциям.');
  }
});

bot.launch().then(() => console.log('Bot is running...')).catch(console.error);
