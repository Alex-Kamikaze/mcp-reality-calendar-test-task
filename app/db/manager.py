from typing import List, Optional
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.data_models import ProductModel
from .models.cache_models import Product
from exceptions.cache_exceptions import CacheException


class CacheManager:
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)

    def add_products(self, products: List[ProductModel]):
        """
        Добавляет в кэш инструменты, которых еще нет в базе

        :param products: Список инструментов с описаниями, которые надо добавить в базу
        """
        try:
            with Session(bind=self.engine) as session:
                with session.begin():
                    for product in products:
                        product_exists = (
                            session.query(Product)
                            .filter_by(name=product.name)
                            .one_or_none()
                        )
                        if not product_exists:
                            new_product = Product(
                                name=product.name, description=product.description
                            )
                            session.add(new_product)
                        else:
                            self.update_product(product)

                    session.commit()
        except SQLAlchemyError:
            raise CacheException()

    def get_product_by_name(self, name: str) -> Optional[ProductModel]:
        """
        Вытаскивает информацию об инструменте из базы по имени

        :param name: Название инструмента
        :return: Информацию об инструменте из кэша
        """

        try:
            with Session(bind=self.engine) as session:
                product = session.query(Product).filter_by(name=name).one_or_none()
                if product is not None:
                    return ProductModel(
                        name=product.name, description=product.description
                    )
                else:
                    return None
        except SQLAlchemyError:
            raise CacheException()

    def update_product(self, product: ProductModel):
        """
        Обновляет информацию об инструменте в базе

        :param product: Инструмент, информацию о котором надо обновить
        """
        try:
            with Session(bind=self.engine) as session:
                product_from_db = (
                    session.query(Product).filter_by(name=product.name).one_or_none()
                )
                if product_from_db is not None:
                    product_from_db.name = product.name
                    product_from_db.description = product.description
                    session.add(product_from_db)
                    session.commit()
        except SQLAlchemyError:
            raise CacheException()

    def get_product_list(self) -> List[str]:
        """
        Возвращает список продуктов, доступных в базе

        :return: Список доступных продуктов
        """
        try:
            with Session(bind=self.engine) as session:
                products = session.query(Product).all()
                return [product.name for product in products]
        except SQLAlchemyError:
            raise CacheException()
