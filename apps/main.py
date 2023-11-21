from fastapi import FastAPI
from ubee_evw_system_info import router as run_system_info_reader_router

app = FastAPI()

app.include_router(run_system_info_reader_router)
