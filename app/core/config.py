from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class ParseSettings(BaseModel):
    url: str = "https://www.cybersport.ru/?sort=-publishedAt"
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }


class TelegramSettings(BaseModel):
    pass


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool =  False
    max_overflow: int = 10
    pool_size: int = 50


class Settings(BaseSettings):
    parse: ParseSettings = ParseSettings()
    run: RunConfig = RunConfig()
    telegram: TelegramSettings = TelegramSettings()
    db: DatabaseConfig

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
