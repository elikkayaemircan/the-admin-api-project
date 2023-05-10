from fastapi import Depends, APIRouter, HTTPException

from . import crud, schemas

from ..config import Settings, get_settings


router = APIRouter(
    prefix="/openmanage",
    tags=["openmanage"],
)


@router.get("/hosts", response_model=schemas.OMESummary)
async def read_hosts(config: Settings = Depends(get_settings), skip: int = 0, top: int = 100):
    """
    Get all hosts registered to Dell OpenManage Enterprise.

    Args:\n
        skip(int): do not bring first n hosts\n
        top(int): show only top n hosts

    Returns: A list of dictionaries which are Dell OpenManage Enterprise hosts.
    """
    api_hosts = await crud.get_hosts(config, skip=skip, top=top)
    if api_hosts is None:
        raise HTTPException(status_code=404, detail="OME Host summary cannot found")
    return api_hosts


@router.get("/id/{id}", response_model=schemas.OMEDetailed)
async def read_id(config: Settings = Depends(get_settings), id: int = 0):
    """
    Get detailed information of a single host from Dell OpenManage Enterprise
    by using its OME unique id.

    Args:
        id(int): unique id of the host given by Dell OpenManage Enterprise.

    Returns: A dictionary of detailed information of the host from Dell OpenManage Enterprise.
    """
    api_id = await crud.get_w_id(config, id=id)
    if api_id is None:
        raise HTTPException(status_code=404, detail="OME Host id not found")
    return api_id
