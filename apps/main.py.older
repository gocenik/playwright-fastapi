# main.py
from fastapi import FastAPI
from ubee_evw_system_info_reader import router as ubee_evw_router

app = FastAPI()

app.include_router(ubee_evw_router, prefix="/ubee_evw")

