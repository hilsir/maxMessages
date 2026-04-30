import os
import time

from dotenv import load_dotenv

from maxbot_api_client_python import API, Config
from maxbot_api_client_python.types.constants import UploadType
from maxbot_api_client_python.types.models import UploadFileReq, SendMessageReq
from maxbot_api_client_python.utils import attach_image

from path_formation import PathManager
# Загружаем конфиг
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
DATA_PATH = os.getenv("DATA_PATH")
TIME_MESSAGES = [t.strip() for t in os.getenv("TIME_MESSAGES").split(",")]

# Настраиваем API
config = Config(
    base_url="https://platform-api.max.ru",
    token=BOT_TOKEN,
    ratelimiter=25,
    timeout=30
)

path_manager = PathManager()

def send_data():
    # Подключение
    with API(config) as bot:
    # все папки с картинками и текстами
        folders_list = path_manager.folders_list()

        for folder_name in folders_list:
            folder_full_path = os.path.join(DATA_PATH, folder_name)

            # Формируем пути к файлам на основе имени папки
            image_path = path_manager.image_path(folder_full_path, folder_name)
            text_path = path_manager.text_path(folder_full_path, folder_name)

            # Проверяем, что оба файла существуют
            if not os.path.exists(image_path) and not os.path.exists(text_path):
                continue

            # Получить текст
            with open(text_path, 'r', encoding='utf-8') as f:
                caption_text = f.read()

            # Объект запроса картинки
            upload_req = UploadFileReq(
                type=UploadType.IMAGE,
                file_path=image_path
            )

            # Отправка картинки на сервер и получть ссылку на неё
            file_info = bot.uploads.upload_file(upload_req)

            if not file_info and not file_info.token:
                continue

            # Собираем сообщение
            message_req = SendMessageReq(
                chat_id=GROUP_ID,
                text=caption_text,
                attachments=[attach_image(token=file_info.token)]  # прекрипили токен картинки
            )

            # Отправляем сообщение
            bot.messages.send_message(message_req)

            # Чтобы спама не было
            time.sleep(1)