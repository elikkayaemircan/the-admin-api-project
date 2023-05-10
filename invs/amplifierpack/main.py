from fastapi import Depends, APIRouter, HTTPException

from . import crud, schemas

from ..config import Settings, get_settings


router = APIRouter(
    prefix="/amplifierpack",
    tags=["amplifierpack"],
)


@router.get("/hosts", response_model=schemas.ILOSummary)
async def read_hosts(config: Settings = Depends(get_settings), skip: int = 0, top: int = 100):
    """
    Get all hosts registered to iLO Amplifier Pack.

    Args:\n
        skip(int): do not bring first n hosts\n
        top(int): show only top n hosts

    Returns: A list of dictionaries which are iLO Amplifier Pack hosts.
    """
    api_hosts = await crud.get_hosts(config, skip=skip, top=top)
    if api_hosts is None:
        raise HTTPException(status_code=404, detail="iLO Amplifier Pack summary cannot found")
    return api_hosts


@router.get("/id/{id}", response_model=schemas.ILODetailed)
async def read_id(config: Settings = Depends(get_settings), id: str = "id"):
    """
    Get detailed information of a single host from iLO Amplifier Pack
    by using its Amplifier Pack unique id.

    Args:\n
        id(str): unique id of the host given by iLO Amplifier Pack.

    Returns: A dictionary of detailed information of the host from iLO Amplifier Pack.
    """
    api_id = await crud.get_w_id(config, id=id.upper())
    if api_id is None:
        raise HTTPException(status_code=404, detail="iLO Amplifier Pack Host id not found")
    return api_id
