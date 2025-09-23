from typing import List
from models.data_models import SectionModel
from models.base_resolver import DataResolver

class GoogleDataResolver(DataResolver):

    def get_data_from_xlsx(token_path: str) -> List[SectionModel]:
        """
        Получает данные из файлов Excel, лежащих на Google-диске

        :param token_path: Путь к токену для авторизации на Google Drive API
        :return: Возвращает список разделов с их именами и описаниями
        """

        pass