from typing import List
from resolvers.remote_product_resolver import GoogleDataResolver
from models.data_models import ProductFromExcelModel

class GoogleDriveResolverService:
    def __init__(self, resolver: GoogleDataResolver):
        self.resolver = resolver

    def __call__(self, file_name: str) -> List[ProductFromExcelModel]:
        return self.resolver.get_data_from_xlsx(file_name)