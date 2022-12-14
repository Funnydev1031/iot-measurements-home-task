import asyncio
import random
from typing import Optional
from fastapi import HTTPException, Query, Request, APIRouter, WebSocket
from fastapi.logger import logger
from starlette.websockets import WebSocketState

from models import Metric, Location, Device


DEVICES_ROUTER = APIRouter(prefix="/devices", tags=["devices"])


@DEVICES_ROUTER.get("/", response_model=list[Device])
def get_devices(
    request: Request,
    id: Optional[list[int]] = Query(default=None),
    name: Optional[list[str]] = Query(default=None),
) -> list[Device]:
    return [
        Device.parse_obj(device) for device in request.app.data["devices"]
        if (not id or device["id"] in id) and (not name or device["name"] in name)
    ]


@DEVICES_ROUTER.get("/{id:int}", response_model=Device)
def get_device_by_id(
    id: int,
    request: Request
) -> Device:
    device = None

    for _device in request.app.data["devices"]:
        if _device["id"] == id:
            device = _device
            break

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found.")

    return Device.parse_obj(device)


@DEVICES_ROUTER.get("/{mac:str}", response_model=Device)
def get_device_by_mac(
    mac: str,
    request: Request
) -> Device:
    device = None

    for _device in request.app.data["devices"]:
        if _device["mac"] == mac:
            device = _device
            break

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found.")

    return Device.parse_obj(device)



LOCATIONS_ROUTER = APIRouter(prefix="/locations", tags=["locations"])


@LOCATIONS_ROUTER.get("/", response_model=list[Location])
def get_locations(
    request: Request,
    id: Optional[list[int]] = Query(default=None),
    name: Optional[list[str]] = Query(default=None),
) -> list[Location]:
    return [
        Location.parse_obj(location) for location in request.app.data["locations"]
        if (not id or location["id"] in id) and (not name or location["name"] in name)
    ]


@LOCATIONS_ROUTER.get("/{id:int}", response_model=Location)
def get_location_by_id(
    id: int,
    request: Request
) -> Location:
    location = None

    for _location in request.app.data["locations"]:
        if _location["id"] == id:
            location = _location
            break

    if location is None:
        raise HTTPException(status_code=404, detail="Location not found.")

    return Location.parse_obj(location)


@LOCATIONS_ROUTER.get("/{name:str}", response_model=Location)
def get_location_by_name(
    name: str,
    request: Request
) -> Location:
    location = None

    for _location in request.app.data["locations"]:
        if _location["name"].lower() == name.lower():
            location = _location
            break

    if location is None:
        raise HTTPException(status_code=404, detail="Location not found.")

    return Location.parse_obj(location)


METRICS_ROUTER = APIRouter(prefix="/metrics", tags=["metrics"])


@METRICS_ROUTER.get("/", response_model=list[Metric])
def get_metrics(
    request: Request,
    id: Optional[list[int]] = Query(default=None),
    name: Optional[list[str]] = Query(default=None),
) -> list[Metric]:
    return [
        Metric.parse_obj(metric) for metric in request.app.data["metrics"]
        if (not id or metric["id"] in id) and (not name or metric["name"] in name)
    ]


@METRICS_ROUTER.get("/{id:int}", response_model=Metric)
def get_metric_by_id(
    id: int,
    request: Request
) -> Metric:
    metric = None

    for _metric in request.app.data["metrics"]:
        if _metric["id"] == id:
            metric = _metric
            break

    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found.")

    return Metric.parse_obj(metric)


@METRICS_ROUTER.get("/{name:str}", response_model=Metric)
def get_metric_by_name(
    name: str,
    request: Request
) -> Metric:
    metric = None

    for _metric in request.app.data["metrics"]:
        if _metric["name"].lower() == name.lower():
            metric = _metric
            break

    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found.")

    return Metric.parse_obj(metric)


MEASUREMENTS_ROUTER = APIRouter(prefix="/measurements", tags=["measurements"])


@MEASUREMENTS_ROUTER.websocket("/ws")
async def measurements_websocket(
    websocket: WebSocket,
) -> None:
    delay = random.uniform(2.5, 5)
    logger.info(f"Accepting connection in {delay:0.1f}s...")
    await asyncio.sleep(delay)
    await websocket.app.measurement_generator.add_connection(websocket)
    await websocket.accept()
    while True:
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()
                logger.debug(f"Websocket message recieved : {data}")
        except:
            await websocket.app.measurement_generator.remove_connection(websocket)
            break