from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_hosts(
        config, db: Session,
        admin_workgroup: str = "ADMINGROUP1",
        detail_level: int = 0,
        status: list = ["PROD"],
        skip: int = 0, top: int = 100
    ):

    if detail_level == 1:

        status = status + ["ODM", "UAT"]

    response = db.query(models.HOST).filter(
        models.HOST.ADMIN == admin_workgroup,
        models.HOST.STATUS.in_(status),
    ).offset(skip).limit(top).all()

    if response != None:

        return {
            "app_name": config.app_name,
            "service_name": config.service_name,
            "module_name": "maindb",
            "timestamp": datetime.now(),
            "response": response,
        }

    return None


def get_w_id(config, db: Session, id: int):

    response = db.query(models.HOST).filter(models.HOST.ID == id).first()

    if response != None:

        return {
            "app_name": config.app_name,
            "service_name": config.service_name,
            "module_name": "maindb",
            "timestamp": datetime.now(),
            "response": [response],
        }

    return None

def get_w_name(config, db: Session, name: str):

    response = db.query(models.HOST).filter(models.HOST.NAME == name).first()

    if response != None:

        return {
            "app_name": config.app_name,
            "service_name": config.service_name,
            "module_name": "maindb",
            "timestamp": datetime.now(),
            "response": [response],
        }

    return None
