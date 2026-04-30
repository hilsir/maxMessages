import os
from dotenv import load_dotenv

class PathManager:
    def __init__(self):
        load_dotenv()
        self.data_path = os.getenv("DATA_PATH")

    # Получаем список всех папок внутри DATA_PATH
    def folders_list(self):
        return [f for f in os.listdir(self.data_path) if os.path.isdir(os.path.join(self.data_path, f))]

    @staticmethod
    def image_path(folder_full_path, folder_name):
        for ext in ['.jpg', '.jpeg', '.png']:
            potential_path = os.path.join(folder_full_path, f"{folder_name}{ext}")
            if os.path.exists(potential_path):
                return potential_path

    @staticmethod
    def text_path(folder_full_path, folder_name):
        return os.path.join(folder_full_path, f"{folder_name}.txt")