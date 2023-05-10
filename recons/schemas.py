from datetime import datetime
from pydantic import BaseModel


class AllBase(BaseModel):
    app_name: str | None = None
    service_name: str | None = None
    module_name: str | None = None
    timestamp: datetime | None = None


class SatelliteBase(BaseModel):
    counts: dict
    duplicated_at_satellite_ids: list
    duplicated_at_satellite_names: list
    remove_at_satellite_ids: list
    remove_at_satellite_names: list
    missing_at_satellite_ids: list
    missing_at_satellite_names: list


class Satellite(AllBase):
    response: SatelliteBase | None = None


class OpenManageBase(BaseModel):
    counts: dict
    duplicated_at_openmanage_ids: list
    duplicated_at_openmanage_identifiers: list
    remove_at_openmanage_ids: list
    remove_at_openmanage_identifiers: list
    missing_at_openmanage_ids: list
    missing_at_openmanage_names: list


class OpenManage(AllBase):
    response: OpenManageBase | None = None


class AmplifierPackBase(BaseModel):
    counts: dict
    duplicated_at_amplifierpack_ids: list
    duplicated_at_amplifierpack_serials: list
    remove_at_amplifierpack_ids: list
    remove_at_amplifierpack_serials: list
    missing_at_amplifierpack_ids: list
    missing_at_amplifierpack_names: list


class AmplifierPack(AllBase):
    response: AmplifierPackBase | None = None


class FusionDirectorBase(BaseModel):
    counts: dict
    duplicated_at_fusiondirector_ids: list
    duplicated_at_fusiondirector_serials: list
    remove_at_fusiondirector_ids: list
    remove_at_fusiondirector_serials: list
    missing_at_fusiondirector_ids: list
    missing_at_fusiondirector_names: list


class FusionDirector(AllBase):
    response: FusionDirectorBase | None = None
