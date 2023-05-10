from datetime import datetime
from pydantic import BaseModel


class AllBase(BaseModel):
    app_name: str | None = None
    service_name: str | None = None
    module_name: str | None = None
    timestamp: datetime | None = None


class SatelliteThin(BaseModel):
    name: str
    id: int


class SatelliteThick(BaseModel):
    name: str
    id: int
    ip: str | None = None
    mac: str | None = None
    operatingsystem_name: str | None = None
    certname: str | None = None
    uptime_seconds: int | None = None
    organization_name: str | None = None
    location_name: str | None = None
    model_name: str | None = None
    errata_status: int | None = None
    errata_status_label: str | None = None
    traces_status: bool | None = None
    traces_status_label: str | None = None
    content_facet_attributes: dict | None = None
    subscription_facet_attributes: dict | None = None
    interfaces: list | None = None
    facts: dict | None = None


class SatelliteSummary(AllBase):
    response: list[SatelliteThin] = []


class SatelliteDetailed(AllBase):
    response: list[SatelliteThick] = []
