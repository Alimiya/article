import google.generativeai as genai

API_KEY="AIzaSyCZQ-h6Gdkiw9B3G50kPRnNQSzOwVFj2Rs"

# Настроим API-ключ для Gemini
genai.configure(api_key=API_KEY)

# Загрузка модели Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def rate_text_using_gemini(transcription, criteria):
    # Формируем сообщение, чтобы отправить запрос с транскрипцией и критериями
    prompt = f"Rate this text: {transcription} by this criteria: {criteria}"

    # Начинаем чат с пустой историей
    chat = model.start_chat(history=[])

    # Отправляем запрос с транскрипцией и критериями
    response = chat.send_message(prompt)

    return response.text

def read_transcription_from_file(file_path):
    """Функция для чтения текста из файла"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

if __name__ == "__main__":
    # Прочитаем текст транскрипции из файла
    transcription = read_transcription_from_file("part1_transcription.txt")
    
    if transcription is None:
        print("Failed to read transcription from file.")
        exit(1)

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
    
    print(f"Rating result:\n{result}")
