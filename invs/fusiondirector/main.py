from fastapi import Depends, APIRouter, HTTPException

from . import crud, schemas

from ..config import Settings, get_settings


router = APIRouter(
    prefix="/fusiondirector",
    tags=["fusiondirector"],
)


@router.get("/hosts", response_model=schemas.BMCSummary)
async def read_hosts(config: Settings = Depends(get_settings), skip: int = 0, top: int = 100):
    """
    Get all hosts registered to Huawei Fusion Director.

    Args:\n
        skip(int): do not bring first n hosts\n
        top(int): show only top n hosts

    Returns: A list of dictionaries which are Huawei Fusion Director hosts.
    """
    api_hosts = await crud.get_hosts(config, skip=skip, top=top)
    if api_hosts is None:
        raise HTTPException(status_code=404, detail="Fusion Director Host summary cannot found")
    return api_hosts


@router.get("/id/{id}", response_model=schemas.BMCDetailed)
async def read_id(config: Settings = Depends(get_settings), id: str = "id"):
    """
    Get detailed information of a single host from Huawei Fusion Director
    by using its Huawei Fusion Director unique id.

    Args:
        id(str): unique id of the host given by Huawei Fusion Director.

    Returns: A dictionary of detailed information of the host from Huawei Fusion Director.
    """
    api_id = await crud.get_w_id(config, id=id)
    if api_id is None:
        raise HTTPException(status_code=404, detail="Fusion Director Host id not found")
    return api_id
