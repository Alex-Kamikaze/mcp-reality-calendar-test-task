from pydantic import BaseModel

class ProductFromExcelModel(BaseModel):
    """
    Инструмент из Excel-файла с ссылкой на описание на отдельной странице
    
    :param name: Название инструмента
    :param link: Ссылка на описание инструмента
    """
    name: str
    link: str

class ProductModel(BaseModel):
    """
    Инструмент с его развернутым описанием, который должна сократить нейросеть

    :param name: Название инструмента
    :param description: Описание инструмента
    """

    name: str
    description: str