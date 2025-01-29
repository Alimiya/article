import google.generativeai as genai
import sys
import os

API_KEY = "AIzaSyCZQ-h6Gdkiw9B3G50kPRnNQSzOwVFj2Rs"

# Настроим API-ключ для Gemini
genai.configure(api_key=API_KEY)

# Загрузка модели Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def rate_text_using_gemini(transcription, criteria):
    """Отправка текста и критериев в модель Gemini для оценки"""
    prompt = f"Rate this text: {transcription} by this criteria: {criteria}"

    # Начинаем чат с пустой историей
    chat = model.start_chat(history=[])

    # Отправляем запрос с транскрипцией и критериями
    response = chat.send_message(prompt)

    return response.text

def read_transcription_from_file(file_path):
    """Функция для чтения текста из файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def save_result_to_file(original_file, result):
    """Сохраняет результат в новый файл с добавлением суффикса '_result'"""
    result_file = original_file.rsplit('.', 1)[0] + "_result.txt"
    try:
        with open(result_file, 'w', encoding='utf-8') as file:
            file.write(result)
        print(f"Result saved to {result_file}")
    except Exception as e:
        print(f"Error saving result to file {result_file}: {e}")

if __name__ == "__main__":
    # Проверяем, передано ли имя файла как аргумент
    if len(sys.argv) < 2:
        print("Usage: python gem.py <transcription_file>")
        sys.exit(1)

    transcription_file = sys.argv[1]

    # Проверяем, существует ли файл
    if not os.path.isfile(transcription_file):
        print(f"File {transcription_file} does not exist.")
        sys.exit(1)

    # Прочитаем текст транскрипции из файла
    transcription = read_transcription_from_file(transcription_file)
    if transcription is None:
        print("Failed to read transcription from file.")
        sys.exit(1)

    # Пример критериев
    criteria = """
first criteria:
 35 points: The response is well-organized, covers all three required elements comprehensively and logically.
 25 points: The speech is organized, covers all elements, but lacks depth in some areas.
 10 points: The speech is somewhat organized but has two key elements or lacks coherence.
 5 points: The speech is poorly organized, having one key element, and lacks coherence
second criteria:
 5 points: Stays within the allotted time, well-paced.
 4 points: Slightly over or under time, mostly well-paced.
 3 points: Significantly over or under time, pacing issues.
 1 points: Does not adhere to the time limit, poorly paced.
third criteria:
 10 points: Extensive and accurate use of vocabulary including language chunks related to the topic of healthcare.
 7 points: Good use of topical vocabulary, with minor errors.
 5 points: Adequate use of vocabulary, but with some errors or omissions.
 2 points: Limited or incorrect use of topical vocabulary. 
fourth criteria:
 10 points: Excellent grammar usage with no errors.
 7 points: Good grammar usage with minor errors.
 5 points: Adequate grammar usage with some errors.
 2 points: Frequent grammatical errors that impede understanding. 
    """

    # Оценка текста через Google Gemini API
    result = rate_text_using_gemini(transcription, criteria)
    
    # Сохраняем результат в новый файл
    save_result_to_file(transcription_file, result)

    print(f"Rating result:\n{result}")

