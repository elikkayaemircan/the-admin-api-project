from datetime import datetime
from pydantic import BaseModel


class AllBase(BaseModel):
    app_name: str | None = None
    service_name: str | None = None
    module_name: str | None = None
    timestamp: datetime | None = None


class OMEThin(BaseModel):
    Identifier: str
    Id: int
    DeviceName: str
    Status: int
    ConnectionState: bool


class OMEThick(BaseModel):
    Identifier: str
    Id: int
    DeviceName: str
    Status: int
    ConnectionState: bool
    Model: str | None = None
    DeviceManagement: list | None = None
    DeviceSpecificData: dict | None = None


class OMESummary(AllBase):
    response: list[OMEThin] = []


class OMEDetailed(AllBase):
    response: list[OMEThick] = []
