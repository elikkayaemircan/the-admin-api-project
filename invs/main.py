from fastapi import FastAPI

import invs.maindb.main as maindb
import invs.satellite.main as satellite
import invs.openmanage.main as openmanage
import invs.amplifierpack.main as amplifierpack
import invs.fusiondirector.main as fusiondirector


app = FastAPI()


app.include_router(maindb.router)
app.include_router(satellite.router)
app.include_router(openmanage.router)
app.include_router(amplifierpack.router)
app.include_router(fusiondirector.router)
