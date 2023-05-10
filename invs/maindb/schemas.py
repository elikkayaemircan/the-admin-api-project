from datetime import datetime
from pydantic import BaseModel


class AllBase(BaseModel):
    app_name: str | None = None
    service_name: str | None = None
    module_name: str | None = None
    timestamp: datetime | None = None


class HOSTThick(BaseModel):
    NAME: str
    ID: int
    STATUS: str
    ADMIN: str | None = None
    CRITICAL: bool

    class Config:
        orm_mode = True


class HOST(AllBase):
    response: list[HOSTThick] = []
