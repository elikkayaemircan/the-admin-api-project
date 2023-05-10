from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from ..config import Settings, get_settings


router = APIRouter(
    prefix="/maindb",
    tags=["maindb"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/hosts", response_model=schemas.HOST)
def read_hosts(config: Settings = Depends(get_settings), db: Session = Depends(get_db),
        admin_workgroup: str = "ADMINGROUP1",
        detail_level: int = 0,
        skip: int = 0, top: int = 100
    ):
    """
    Get all hosts from MAIN Database.

    Args:\n
        admin_workgroup(str): show hosts of admin workgroup\n
        skip(int): do not bring first n hosts\n
        top(int): show only top n hosts

    Returns: A list of dictionaries which are MAINDB hosts.
    """
    db_hosts = crud.get_hosts(config, db, admin_workgroup=admin_workgroup, detail_level=detail_level, skip=skip, top=top)
    if db_hosts is None:
        raise HTTPException(status_code=404, detail="No HOST found with search criteria")
    return db_hosts


@router.get("/id/{id}", response_model=schemas.HOST)
def read_cinum(config: Settings = Depends(get_settings), db: Session = Depends(get_db), id: int = 0 ):
    """
    Get detailed information of a single host from MAIN Database
    by using its unique ID.

    Args:
        id(int): unique ID of the host given by MAINDB.

    Returns: A dictionary of detailed information of the host from MAINDB.
    """
    db_id = crud.get_w_id(config, db, cinum=cinum)
    if db_id is None:
        raise HTTPException(status_code=404, detail="HOST id number not found")
    return db_id


@router.get("/name/{name}", response_model=schemas.HOST)
def read_ciname(config: Settings = Depends(get_settings), db: Session = Depends(get_db), name: str = "name" ):
    """
    Get detailed information of a single host from MAIN Database
    by using its unique NAME.

    Args:
        name(str): unique NAME of the host given by MAINDB.

    Returns: A dictionary of detailed information of the host from MAINDB.
    """
    db_name = crud.get_w_name(config, db, ciname=name.upper())
    if db_name is None:
        raise HTTPException(status_code=404, detail="HOST name not found")
    return db_name
