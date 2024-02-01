#pip install opencv-python
#pip install pytesseract
# import cv2
# import pytesseract

# # Загрузка видеофайла
# video = cv2.VideoCapture('Блиц - скорость без границ, ленивцы ZVEROPOLIS.mp4')
#
# # Проверка, открыт ли файл видео
# if not video.isOpened():
#     print("Не удалось открыть видео")
#     exit()
#
# # Загрузка Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
# while True:
#     # Чтение каждого кадра видео
#     ret, frame = video.read()
#
#     # Проверка, достигнут ли конец видео
#     if not ret:
#         break
#
#     # Преобразование кадра в черно-белое изображение (если необходимо)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Выполнение OCR для определения текста
#     text = pytesseract.image_to_string(gray)
#
#     # Вывод определенного текста
#     print(text)
#
#     # Отображение кадра видео
#     cv2.imshow('Video', frame)
#
#     # Если нажата клавиша 'q', прервать цикл
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Освобождение ресурсов
# video.release()
# cv2.destroyAllWindows()






# Загружаем видео
# video_path = 'Блиц - скорость без границ, ленивцы ZVEROPOLIS.mp4'
# cap = cv2.VideoCapture(video_path)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# # Проверяем, успешно ли открыт видео файл
# if cap.isOpened():
#     # Получаем информацию о видео
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#
#     # Создаем окно для отображения видео
#     cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
#
#     while True:
#         # Считываем кадр из видео
#         ret, frame = cap.read()
#
#         if ret:
#             # Преобразуем кадр в оттенки серого
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#             # Используем pytesseract для распознавания текста на кадре
#             text = pytesseract.image_to_string(gray)
#
#             # Выводим распознанный текст на кадре
#             cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#             # Отображаем кадр в окне
#             cv2.imshow('Video', frame)
#
#             # Ожидаем нажатия клавиши 'q' для выхода из цикла
#             if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
#                 break
#         else:
#             break
#
#     # Закрываем окно и освобождаем видео поток
#     cap.release()
#     cv2.destroyAllWindows()
#
# else:
#     print("Ошибка при открытии видео файла")


import cv2
import easyocr
import numpy as np
from translate import Translator
import moviepy.editor as mp


# Загрузка видеофайла
video = cv2.VideoCapture('3.mp4')
# Функция перевода текста на русский язык
def translate_text(text):
    translator = Translator(to_lang="ru")
    translation = translator.translate(text.lower())
    print(translation)
    return translation

# Проверка, открыт ли файл видео
if not video.isOpened():
    print("Не удалось открыть видео")
    exit()
# Получение информации о видео
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))
num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
# Инициализация EasyOCR
reader = easyocr.Reader(['en'], gpu=True)
# Создание объекта VideoWriter для сохранения обработанного видео
output_video = cv2.VideoWriter('111.mp4',
                               cv2.VideoWriter_fourcc(*'XVID'),
                               fps, (frame_width, frame_height))

# Сохранение аудиодорожки в файл
clip = mp.VideoFileClip('3.mp4')
audio = clip.audio
audio.write_audiofile('audio1.mp3')

while True:
    # Чтение каждого кадра видео
    ret, frame = video.read()
    # Проверка, достигнут ли конец видео
    if not ret:
        break
    # Обнаружение текста с помощью EasyOCR
    results = reader.readtext(frame)
    threshold = 0.25

    # Вывод прямоугольников и текста на кадре
    for t_, t in enumerate(results):
        bbox, text, score = t
        if score > threshold:
            translated_text = translate_text(text)
            print(text)
            # cv2.rectangle(frame, bbox[0], bbox[2], (0, 255, 0), 5)
            bbox = np.array(bbox, dtype=int)
            text_size, _ = cv2.getTextSize(translated_text, cv2.FONT_HERSHEY_COMPLEX, 1, 2)
            text_x = bbox[0][0]
            text_y = bbox[0][1] - text_size[1] // 2  # Выравнивание текста по центру прямоугольника по вертикали
            font_size = 1.5
            font_color = (0, 255, 0)  # Зеленый цвет
            font_thickness = 2
            font_style = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, translated_text, (text_x, text_y), font_style, font_size, font_color, font_thickness)
    # Запись обработанного кадра в выходное видео
    output_video.write(frame)

# Освобождение ресурсов
video.release()
output_video.release()
cv2.destroyAllWindows()

# Создание объекта VideoFileClip для исходного видео и аудиодорожки
video_clip = mp.VideoFileClip('111.mp4')
audio_clip = mp.AudioFileClip('audio1.mp3')

# Объединение видео и аудио
final_clip = video_clip.set_audio(audio_clip)

# Сохранение окончательного видео
final_clip.write_videofile('final_video.mp4')





# import cv2
# import pytesseract
# import easyocr
# import matplotlib.pyplot as plt
# import numpy as np
# from google.colab.patches import cv2_imshow
# from translate import Translator
# import moviepy.editor as mp
#
# # Загрузка видеофайла
# video = mp.VideoFileClip('/content/drive/MyDrive/Блиц - скорость без границ, ленивцы ZVEROPOLIS.mp4')
#
# # Функция перевода текста на русский язык
# def translate_text(text):
#     translator = Translator(to_lang="ru")
#     translation = translator.translate(text)
#     return translation
#
# # Инициализация EasyOCR
# reader = easyocr.Reader(['en'], gpu=True)
#
# # Сохранение аудиодорожки в файл
# audio = video.audio
# audio.write_audiofile('/content/drive/MyDrive/audio.mp3')
#
# # Функция обработки кадра
# def process_frame(frame):
#     # Обнаружение текста с помощью EasyOCR
#     results = reader.readtext(frame)
#
#     threshold = 0.25
#
#     # Вывод прямоугольников и текста на кадре
#     for t_, t in enumerate(results):
#         print(t)
#
#         bbox, text, score = t
#
#         if score > threshold:
#             print(bbox[0])
#             translated_text = translate_text(text)  # Перевод текста на русский
#             cv2.putText(frame, translated_text, (int(bbox[0][0]), int(bbox[0][1])), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
#
#     return frame
#
# # Обработка кадров видео
# processed_video = video.fl_image(process_frame)
#
# # Сохранение обработанного видео
# processed_video.write_videofile('/content/drive/MyDrive/final_video.mp4')