import os
import time

from dotenv import load_dotenv

from maxbot_api_client_python import API, Config
from maxbot_api_client_python.types.constants import UploadType
from maxbot_api_client_python.types.models import UploadFileReq, SendMessageReq
from maxbot_api_client_python.utils import attach_image, attach_file

from path_formation import PathManager
# Загружаем конфиг
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
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

        for folder_full_path in folders_list:
            folder_name = os.path.basename(folder_full_path)

            # Формируем пути к файлам на основе имени папки
            image_path = path_manager.image_path(folder_full_path, folder_name)
            text_path = path_manager.text_path(folder_full_path, folder_name)

            # Проверяем, что оба файла существуют
            if not image_path or not os.path.exists(text_path):
                continue

            # Объект запроса картинки
            image_upload_req = UploadFileReq(
                type=UploadType.IMAGE,
                file_path=image_path
            )

            # Отправка картинки на сервер и получть ссылку на неё
            image_info = bot.uploads.upload_file(image_upload_req)

            if not image_info and not image_info.token:
                continue

            # Объект запроса текстового файла
            text_upload_req = UploadFileReq(
                type=UploadType.FILE,
                file_path=text_path
            )

            # Отправка текстового файла на сервер и получить ссылку на него
            text_info = bot.uploads.upload_file(text_upload_req)

            if not text_info and not text_info.token:
                continue

            # MAX API не позволяет прикладывать файл вместе с картинкой
            # в одном сообщении, поэтому отправляем их отдельными сообщениями

            # Сообщение с картинкой
            image_message_req = SendMessageReq(
                chat_id=GROUP_ID,
                attachments=[attach_image(token=image_info.token)]
            )
            bot.messages.send_message(image_message_req)

            time.sleep(1)

            # Сообщение с текстовым файлом
            text_message_req = SendMessageReq(
                chat_id=GROUP_ID,
                attachments=[attach_file(token=text_info.token, filename=os.path.basename(text_path))]
            )
            bot.messages.send_message(text_message_req)

            # Чтобы спама не было
            time.sleep(10)