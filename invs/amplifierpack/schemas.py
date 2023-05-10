from datetime import datetime
from pydantic import BaseModel


class AllBase(BaseModel):
    app_name: str | None = None
    service_name: str | None = None
    module_name: str | None = None
    timestamp: datetime | None = None


class ILOThin(BaseModel):
    SerialNumber: str | None = None
    Id: str
    HostName: str | None = None
    PowerState: str | None = None
    Status: dict | None = None

    
class ILOThick(BaseModel):
    SerialNumber: str | None = None
    Id: str
    HostName: str | None = None
    PowerState: str | None = None
    Status: dict | None = None
    Model: str | None = None
    SKU: str | None = None
    MemorySummary: dict | None = None
    ProcessorSummary: dict | None = None


class ILOSummary(AllBase):
    response: list[ILOThin] = []


class ILODetailed(AllBase):
    response: list[ILOThick] = []
