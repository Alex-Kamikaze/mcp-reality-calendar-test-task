from typing import List
from models.base_resolver import DataResolver
from models.data_models import SectionModel

class LocalDataResolver(DataResolver):
    """Класс для получения данных из локальных XLSX-файлов, для тестирования и мока"""

    def get_data_from_xlsx(path: str) -> List[SectionModel]:
        """
        Получение данных из локальных Excel-файлов

        
        :param path: Путь до файла
        :return: Возвращает список разделов с их именами и описаниями
        """
        pass