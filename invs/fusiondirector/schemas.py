from datetime import datetime
from pydantic import BaseModel


class AllBase(BaseModel):
    app_name: str | None = None
    service_name: str | None = None
    module_name: str | None = None
    timestamp: datetime | None = None


class BMCThin(BaseModel):
    SerialNumber: str | None = None
    DeviceID: str
    PowerState: str | None = None
    Status: dict | None = None
    State: str | None = None
    ServerState: str | None = None


class BMCThick(BaseModel):
    SerialNumber: str | None = None
    DeviceID: str
    PowerState: str | None = None
    Status: dict | None = None
    State: str | None = None
    ServerState: str | None = None
    Model: str | None = None
    BiosVersion: str | None = None
    LastMockEventTest: dict | None = None
    IPAddress: str | None = None
    MemorySummary: dict | None = None
    ProcessorSummary: list | None = None
    NetworkAdapterSummary: dict | None = None
    StorageSummary: dict | None = None
    GPUSummary: dict | None = None
    FPGASummary: dict | None = None
    Oem: dict | None = None


class BMCSummary(AllBase):
    response: list[BMCThin] = []


class BMCDetailed(AllBase):
    response: list[BMCThick] = []
