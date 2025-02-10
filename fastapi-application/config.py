from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    __model_config__ = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="",
        env_nested_delimiter="__",
        env_file=(".env.template", ".env"),
    )

    db: DbSettings
    api_prefix: str = "/api"
    run: RunConfig = RunConfig()


settings = Settings()
