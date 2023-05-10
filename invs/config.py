from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):

    app_name: str = "The Admin API Project"
    service_name: str = "INVS inventory services"

    maindb_user: str = "dbuser"
    maindb_pass: str = "dbpass"
    maindb_host: str = "dbhost"
    maindb_port: str = "dbport"
    maindb_name: str = "dbname"

    satellite_host: str = "satellitehost"
    satellite_user: str = "satelliteuser"
    satellite_pass: str = "satellitepass"

    idrac_host: str = "openmanageentp"
    idrac_user: str = "openmanageuser"
    idrac_pass: str = "openmanagepass"

    ilo_host: str = "amplifierpack"
    ilo_user: str = "amplifieruser"
    ilo_pass: str = "amplifierpass"

    ibmc_host: str = "fusiondrct"
    ibmc_user: str = "fusionuser"
    ibmc_pass: str = "fusionpass"

    class Config:
        env_file = "invs/.env"


@lru_cache()
def get_settings():
    return Settings()
