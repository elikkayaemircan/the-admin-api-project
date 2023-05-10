from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import Settings, get_settings


config = get_settings()

SQLALCHEMY_DATABASE_URL = f"""database+engine://\
{config.maindb_user}\
:{config.maindb_pass}\
@{config.maindb_host}\
:{config.maindb_port}\
/{config.maindb_name}"""

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
