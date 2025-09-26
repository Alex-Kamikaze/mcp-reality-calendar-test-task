from typing import Optional, List
from resolvers.remote_product_resolver import GoogleDataResolver
from resolvers.remote_description_resolver import RemoteProductDescriptionResolver
from services.excel_service import GoogleDriveResolverService
from db.manager import CacheManager
from models.data_models import ProductModel

class ProductInfoService:
    """
    Основной сервис бизнес-логики для работы с инструментами и их описаниями
    """

    def __init__(self, db_uri: str, creds_path: str):
        """
        Конструктор 
        
        :param db_uri: URI для подключения к базе данных
        :param creds_path: Путь до файла с credentials'ами для Google Drive API
        """
        self.resolver = GoogleDriveResolverService(GoogleDataResolver(creds_path))
        self.cache = CacheManager(db_uri)
        self.description_resolver = RemoteProductDescriptionResolver()


    def refresh_cache(self, file_name: str):
        """
        Обновляет данные в кэше

        :param file_name: Название Excel-файла, в котором будет информация об инструментах
        """
        products = self.resolver(file_name)
        product_models = [ProductModel(name=product.name, description=self.description_resolver.get_product_description_from_link(product.link)) for product in products]
        self.cache.add_products(product_models)

    def get_product(self, name: str) -> Optional[ProductModel]:
        """
        Получает информацию об инструменте из кэша

        :param name: Название инструмента
        :return: Название инструмента и его описание
        """
        return self.cache.get_product_by_name(name)
    
    def list_products(self) -> List[str]:
        """
        Возвращает список доступных продуктов из базы

        :return: Список продуктов в базе
        """
        return self.cache.get_product_list()