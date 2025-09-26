from abc import ABC, abstractmethod
from .data_models import ProductFromExcelModel
from typing import List


class DataResolver(ABC):
    """
    Интерфейс для классов, которые будут отвечать за получение информации из Excel
    """

    @abstractmethod
    def get_data_from_xlsx() -> List[ProductFromExcelModel]:
        """
        Получение данных из Excel-файла


        :return: Список инструментов с ссылками на их описание
        """
        raise NotImplementedError
