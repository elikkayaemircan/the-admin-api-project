from fastapi import Depends, APIRouter, HTTPException

from . import crud, schemas

from ..config import Settings, get_settings


router = APIRouter(
    prefix="/satellite",
    tags=["satellite"],
)


@router.get("/hosts", response_model=schemas.SatelliteSummary)
async def read_hosts(config: Settings = Depends(get_settings), per_page: int = 100, page: int = 1):
    """
    Get all hosts registered to Red Hat Satellite.

    Args:\n
        per_page(int): bring n hosts in a single page\n
        page(int): show page n

    Returns: A list of dictionaries which are Red Hat Satellite hosts.
    """
    api_hosts = await crud.get_hosts(config, per_page=per_page, page=page)
    if api_hosts is None:
        raise HTTPException(status_code=404, detail="Satellite Host summary cannot found")
    return api_hosts


@router.get("/id/{id}", response_model=schemas.SatelliteDetailed)
async def read_id(config: Settings = Depends(get_settings), id: int = 0):
    """
    Get detailed information of a single host from Red Hat Satellite
    by using its Satellite unique id.

    Args:
        id(int): unique id of the host given by Red Hat Satellite.

    Returns: A dictionary of detailed information of the host from Red Hat Satellite.
    """
    api_id = await crud.get_w_id(config, id=id)
    if api_id is None:
        raise HTTPException(status_code=404, detail="Satellite Host id cannot found")
    return api_id


@router.get("/host/{name}", response_model=schemas.SatelliteDetailed)
async def read_name(config: Settings = Depends(get_settings), name: str = "name"):
    """
    Get detailed information of a single host from Red Hat Satellite
    by using its Satellite unique name.

    Args:
        name(str): unique name of the host given by Red Hat Satellite but mostly the hostname.

    Returns: A dictionary of detailed information of the host from Red Hat Satellite.
    """
    api_name = await crud.get_w_name(config, name=name)
    if api_name is None:
        raise HTTPException(status_code=404, detail="Satellite Host name cannot found")
    return api_name
