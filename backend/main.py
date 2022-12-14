import asyncio
import os
import yaml
import logging
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware

from routes import LOCATIONS_ROUTER, DEVICES_ROUTER, METRICS_ROUTER, MEASUREMENTS_ROUTER
from middleware import RandomFailureMiddleware
from measurement_generator import MeasurementGenerator

uvicorn_logger = logging.getLogger('uvicorn')
logger.handlers = uvicorn_logger.handlers
logger.setLevel(logging.INFO)

app = FastAPI()

with open(f"{os.getcwd()}/data.yaml", "r") as stream:
    app.data = yaml.safe_load(stream)

app.add_middleware(RandomFailureMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(DEVICES_ROUTER)
app.include_router(METRICS_ROUTER)
app.include_router(MEASUREMENTS_ROUTER)
app.include_router(LOCATIONS_ROUTER)

app.measurement_generator = MeasurementGenerator(app)

@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(app.measurement_generator.start())