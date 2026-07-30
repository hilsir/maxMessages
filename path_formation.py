import os
from dotenv import load_dotenv

class PathManager:
    def __init__(self):
        load_dotenv()
        self.data_path = os.getenv("DATA_PATH")

    # Рекурсивно обходим все вложенные папки DATA_PATH и возвращаем
    # только конечные папки (те, где лежат файлы с именем самой папки)
    def folders_list(self):
        leaf_folders = []
        for root, _, _ in os.walk(self.data_path):
            folder_name = os.path.basename(root)
            if os.path.exists(self.text_path(root, folder_name)) or self.image_path(root, folder_name):
                leaf_folders.append(root)
        return leaf_folders

    @staticmethod
    def image_path(folder_full_path, folder_name):
        for ext in ['.jpg', '.jpeg', '.png']:
            potential_path = os.path.join(folder_full_path, f"{folder_name}{ext}")
            if os.path.exists(potential_path):
                return potential_path

    @staticmethod
    def text_path(folder_full_path, folder_name):
        return os.path.join(folder_full_path, f"{folder_name}.txt")