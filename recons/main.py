from fastapi import Depends, FastAPI, HTTPException

from . import schemas, reconciler

from .config import Settings, get_settings


app = FastAPI()


@app.get("/satellite", response_model=schemas.Satellite)
async def read_report(config: Settings = Depends(get_settings)):
    reconcilable = reconciler.Satellite(config)
    await reconcilable.get_data()
    report = reconcilable.reconcile()
    if report['response'] is None:
        raise HTTPException(status_code=404, detail="No reconcilable found for satellite")
    return report

@app.get("/openmanage", response_model=schemas.OpenManage)
async def read_report(config: Settings = Depends(get_settings)):
    reconcilable = reconciler.OpenManage(config)
    await reconcilable.get_data()
    report = reconcilable.reconcile()
    if report['response'] is None:
        raise HTTPException(status_code=404, detail="No reconcilable found for openmanage")
    return report

@app.get("/amplifierpack", response_model=schemas.AmplifierPack)
async def read_report(config: Settings = Depends(get_settings)):
    reconcilable = reconciler.AmplifierPack(config)
    await reconcilable.get_data()
    report = reconcilable.reconcile()
    if report['response'] is None:
        raise HTTPException(status_code=404, detail="No reconcilable found for amplifierpack")
    return report

@app.get("/fusiondirector", response_model=schemas.FusionDirector)
async def read_report(config: Settings = Depends(get_settings)):
    reconcilable = reconciler.FusionDirector(config)
    await reconcilable.get_data()
    report = reconcilable.reconcile()
    if report['response'] is None:
        raise HTTPException(status_code=404, detail="No reconcilable found for fusiondirector")
    return report
