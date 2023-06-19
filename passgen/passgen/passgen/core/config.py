from pydantic import BaseModel
from functools import cached_property


class BotConfig(BaseModel):
    token: str


class DatabaseConfig(BaseModel):
    host: str
    port: int
    password: str
    user: str
    db_name: str
    driver: str = "asyncpg"
    sync_driver: str = "psycopg2"

    @property
    def url(self) -> str:
        return f"postgresql+{self.driver}://{self.user}:{self.password}@"\
            f"{self.host}:{self.port}/{self.db_name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+{self.sync_driver}://{self.user}:{self.password}@"\
            f"{self.host}:{self.port}/{self.db_name}"

    class Config:
        keey_untouched = (cached_property,)


class IntegrationsConfig(BaseModel):
    pass_storage: DatabaseConfig


class Config(BaseModel):
    bot: BotConfig
    integrations: IntegrationsConfig
