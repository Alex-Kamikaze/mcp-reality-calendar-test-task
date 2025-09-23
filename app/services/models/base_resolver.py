from abc import ABC, abstractmethod
from .data_models import SectionModel
from typing import List


class DataResolver(ABC):
    """
    Базовый класс для всех классов, которые будут отвечать за получение информации из Excel
    """

    @abstractmethod
    def get_data_from_xlsx() -> List[SectionModel]:
        """
        Получение данных из Excel-файла


        :return: Список разделов с их описанием
        """
        raise NotImplementedError
