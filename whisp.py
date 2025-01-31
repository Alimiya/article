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
            .output(output_file, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
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
if not audio_file.lower().endswith('.wav'):
    print(f"Input file is not a WAV file. Converting {audio_file} to WAV format.")
    audio_file = convert_to_wav(audio_file)
audio_parts = split_audio(audio_file)
full_transcription = ""

for part in audio_parts:
    print(f"Transcribing {part}...")
    try:
        transcription = transcribe_audio(part)
        full_transcription += transcription + " "
        os.remove(part)
    except Exception as e:
        print(f"Error transcribing {part}: {e}", file=sys.stderr)

output_file = audio_file.rsplit('.', 1)[0] + "_transcription.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(full_transcription)

print(f"\nFull transcription saved to {output_file}")
