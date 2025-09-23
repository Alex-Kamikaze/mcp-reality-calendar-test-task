from pydantic import BaseModel

class SectionModel(BaseModel):
    """
    Дата-класс для модели разделов из Excel-файлов
    
    :param name: Название раздела
    :param description: Описание раздела
    """
    name: str
    description: str