from typing import List
from mcp.server.fastmcp import FastMCP
from services.product_info_service import ProductInfoService
from core.settings import app_settings
from exceptions.cache_exceptions import CacheException

app = FastMCP(name="RealityCalendar MCP")

def provide_service() -> ProductInfoService:
    """
    Предоставляет сервис для работы с кэшом (аля Инъекция Зависимостей)

    :return: Сервис для работы с кэшом
    """
    return ProductInfoService(app_settings.database_uri, app_settings.credentials_path)

@app.resource("products://list",name="get_products")
def get_product_list() -> str:
    """
    Возвращает список продуктов, доступных в базе


    :return: Список продуктов в базе
    """

    try:
        service = provide_service()
        products = service.list_products()
        return ", ".join(products)
    except CacheException:
        return "Не удалось загрузить список продуктов из-за внутренней ошибки"


@app.resource("products://{name}", name="get_product_description")
def get_product_description(name: str) -> str:
    """
    Предоставляет информацию об инструменте с сайта RealityCalendar 
    

    :param name: Название инструмента, информацию о котором необходимо получить
    :return: Описание инструмента с сайта RealityCalendar
    """

    try:
        service = provide_service()
        product = service.get_product(name.encode("utf-8"))
        if product is None:
            return f"Информация об {name} не была найдена"
        else:
            return product.description
    except CacheException:
        return "Не удалось загрузить информацию из кэша из-за внутренней ошибки. Повторите запрос позже"

@app.tool()
def list_products() -> List[str]:
    """
    Возвращает список всех доступных продуктов в базе данных
    
    :return: Список названий продуктов
    """
    try:
        service = provide_service()
        products = service.list_products()
        return products
    except CacheException:
        return ["Не удалось загрузить список продуктов из-за внутренней ошибки"]

@app.tool()
def get_product_info(name: str) -> str:
    """
    Получает подробную информацию о продукте по его названию
    
    :param name: Название продукта
    :return: Описание продукта с официального сайта
    """
    try:
        service = provide_service()
        product = service.get_product(name)
        if product is None:
            return f"Информация о продукте '{name}' не была найдена в базе данных"
        else:
            return f"Продукт: {product.name}\n\nОписание:\n{product.description}"
    except CacheException:
        return "Не удалось загрузить информацию из кэша из-за внутренней ошибки. Повторите запрос позже"

@app.prompt(name="get_product_summarized_information")
def summarize_product_information(name: str) -> str:
    """
    Генерирует промпт для суммирования информации о продукте

    :param name: Название продукта
    :return: Промпт для суммирования информации о продукте
    """

    try: 
        service = provide_service()
        product = service.get_product(name)
        if product is not None:
            return f"Перескажи в краткой форме информацию о продукте {name} по описанию с официального сайта: {product.description}"
        else:
            return f"Не найдено продукта с имененем {name}. Возможные причины: неправильное название, отсутвие продукта в базе. Проверьте правильность названия продукта и попробуйте еще раз"
    except CacheException:
        return "Произошла внутренняя ошибка. Попробуйте повторить запрос позже"
