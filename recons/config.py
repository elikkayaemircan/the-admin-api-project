from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):

    app_name: str = "The Admin API Project"
    service_name: str = "RECONS reconciliation services"

    invs_endpoint: str = "uri"

    class Config:
        env_file = "recons/.env"


@lru_cache()
def get_settings():
    return Settings()
