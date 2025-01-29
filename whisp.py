import sys
import os
import whisper
from pydub import AudioSegment
import ffmpeg

def convert_to_wav(input_file):
    output_file = input_file.rsplit('.', 1)[0] + ".wav"
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format='wav', acodec='pcm_s16le', ac=1, ar='16000')  # Конвертация в 16kHz, моно
            .run()
        )
        print(f"Converted {input_file} to {output_file}")
    except ffmpeg.Error as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)
    return output_file

def split_audio(input_file, duration_ms=30000):
    audio = AudioSegment.from_wav(input_file)
    audio_length = len(audio)
    
    if audio_length <= duration_ms:
        return [input_file]
    
    # Разделяем на части по 30 секунд
    parts = []
    for i in range(0, audio_length, duration_ms):
        part_file = f"{input_file.rsplit('.', 1)[0]}_part{i // duration_ms + 1}.wav"
        audio[i:i + duration_ms].export(part_file, format="wav")
        parts.append(part_file)
    
    return parts

def transcribe_audio(file):
    model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]

if len(sys.argv) < 2:
    print("Usage: python3 transcribe.py <audio_file>")
    sys.exit(1)

audio_file = sys.argv[1]

# Проверяем формат файла
if not audio_file.lower().endswith('.wav'):
    print(f"Input file is not a WAV file. Converting {audio_file} to WAV format.")
    audio_file = convert_to_wav(audio_file)

# Разделяем на части, если длина файла больше 30 секунд
audio_parts = split_audio(audio_file)

# Переменная для накопления всего текста
full_transcription = ""

# Транскрибируем каждую часть
for part in audio_parts:
    print(f"Transcribing {part}...")
    try:
        transcription = transcribe_audio(part)
        full_transcription += transcription + " "  # Добавляем транскрипцию каждой части
        os.remove(part)  # Удаляем часть после транскрибирования
    except Exception as e:
        print(f"Error transcribing {part}: {e}", file=sys.stderr)

# Сохраняем полную транскрипцию в файл
output_file = audio_file.rsplit('.', 1)[0] + "_transcription.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(full_transcription)

print(f"\nFull transcription saved to {output_file}")
