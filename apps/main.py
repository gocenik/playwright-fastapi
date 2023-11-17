from fastapi import FastAPI
from run_system_info_reader import router as run_system_info_reader_router

app = FastAPI()

app.include_router(run_system_info_reader_router)
