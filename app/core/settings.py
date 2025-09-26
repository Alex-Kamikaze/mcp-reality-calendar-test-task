from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, ValidationError


class Settings(BaseSettings):
    """
    Настройки приложения

    :param database_uri: URI для подключения к базе кэша
    :param credentials_path: Путь к файлу credentials.json
    :param filename: Название файла с информацией о разделах
    """

    database_uri: str = Field(alias="DATABASE_URI")
    credentials_path: str = Field(alias="CREDENTIALS_PATH")
    filename: str = Field(alias="FILENAME")
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("database_uri")
    @classmethod
    def validate_database_uri(cls, value: str) -> str:
        if not value.startswith("sqlite://"):
            raise ValidationError("Неправильный URL для подключения")

        if not value.split("///")[-1].endswith((".db", ".sqlite", ".sqlite3")):
            raise ValidationError("Неправильное расширение файла базы данных")

        return value

    @field_validator("credentials_path")
    @classmethod
    def validate_credentials_path(cls, value: str) -> str:
        path = Path(value)

        if path.name not in ("credentials.json", "token.json"):
            raise ValidationError("Файл должен называться credentials.json или token.json")

        if not path.parent.exists():
            raise ValidationError("Путь не существует")

        return value

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str):
        if not value.endswith(".xlsx"):
            raise ValidationError("Файл должен быть с расширением .xlsx")

        return value
    
app_settings = Settings()