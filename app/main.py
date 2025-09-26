import logging
from core.settings import app_settings
from api.mcp_handlers import app
from sqlalchemy.engine import create_engine
from db.models.cache_models import Model
from services.product_info_service import ProductInfoService
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

service = ProductInfoService(app_settings.database_uri, app_settings.credentials_path)

def refresh_cache():
    service.refresh_cache(app_settings.filename)

engine = create_engine(app_settings.database_uri)
Model.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler(jobstores={"default": SQLAlchemyJobStore(url=app_settings.database_uri)})
scheduler.add_job(refresh_cache, "interval", days=1, id="refresh_cache_job")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    service.refresh_cache(app_settings.filename)
    scheduler.start()
    app.run(transport="sse")