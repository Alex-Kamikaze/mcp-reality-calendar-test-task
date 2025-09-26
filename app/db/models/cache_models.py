from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import DeclarativeBase

class Model(DeclarativeBase): ...

class Product(Model):
    """
    Информация о разделе с описанием внутри кэша

    :param name: Название раздела
    :param description: Описание раздела
    """
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    def __str__(self):
        return self.name
