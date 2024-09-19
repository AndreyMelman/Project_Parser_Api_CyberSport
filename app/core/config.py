from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, SecretStr


class ParseSettings(BaseModel):
    url: str = "https://www.cybersport.ru/?sort=-publishedAt"
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }


class TelegramSettings(BaseModel):
    token: SecretStr
    id: SecretStr

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class Settings(BaseSettings):
    parse: ParseSettings = ParseSettings()
    db: DatabaseConfig
    token: TelegramSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file_encoding="utf-8",
    )


settings = Settings()
