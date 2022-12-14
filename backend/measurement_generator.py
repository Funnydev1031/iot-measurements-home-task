import asyncio
import random
from enum import Enum
from typing import Optional, Union
from fastapi import FastAPI, WebSocket
from fastapi.logger import logger
from starlette.websockets import WebSocketState
from pydantic import BaseModel
from datetime import datetime, timedelta

from models import Metric, Location, Device

MESSAGE_PERIOD = [0.8, 1.2]
MESSAGE_GAP = [MESSAGE_PERIOD[0] * 0.1, MESSAGE_PERIOD[1] * 0.1]

DISCONNECT_RATE = 0.00
DEVICE_DISCONNECT_RATE = 0.05
DEVICE_DISCONNECT_PERIOD = [10, 30]

DOOR_OPEN_ID = 1
DOOR_OPEN_UPDATE_PERIOD = [2, 5]

TEMPERATURE_ID = 2
TEMPERATURE_RANGE = [19, 22]
TEMPERATURE_UPDATE_PERIOD = [2, 5]

WIFI_STRENGTH_ID = 3
WIFI_STRENGTH_RANGE = [50, 90]
WIFI_STRENGTH_UPDATE_PERIOD = [2, 5]

WIFI_SSID_ID = 4
WIFI_SSID_OPTIONS = ["Panic At The Cisco", "Drop It Like Its Hotspot", "Wu-Tang LAN", "It Burns When IP", "The WAN and only"]
WIFI_SSID_UPDATE_PERIOD = [20, 60]


class DeviceMeta(BaseModel):
    reconnect_at: Optional[datetime] = None
    last_measurement: dict[int, datetime] = {}

class MessageTypeEnum(Enum):
    ERROR = 'ERROR'
    PING = 'PING'
    MEASUREMENT = 'MEASUREMENT'

# Disabled ... for now
CAPITALISE_MAC_RATE = 0.00

class Message(BaseModel):
    type: MessageTypeEnum
    mac: str

    def serialise(self) -> list:
        return [self.type.value, self.mac.upper() if random.random() < CAPITALISE_MAC_RATE  else self.mac]

class ErrorMessage(Message):
    message: str

    def serialise(self) -> list:
        return [*super().serialise(), self.message]
        

class PingMessage(Message):
    pass

NULL_VALUE_RATE = 0.01

class MeasurementMessage(Message):
    metric: str
    value: Union[bool, float, int, str, None]
    tags: list[str]

    def serialise(self) -> list:
        return [*super().serialise(), self.metric, None if random.random() < NULL_VALUE_RATE else self.value, self.tags]

class MeasurementGenerator:
    devices: dict[int, Device]
    locations: dict[int, Location]
    metrics: dict[int, Metric]
    websockets: list[WebSocket]

    device_meta: dict[int, DeviceMeta]

    def __init__(self, app: FastAPI):
        self.devices = {device["id"]: Device.parse_obj(device) for device in app.data["devices"]}
        self.locations = {location["id"]: Location.parse_obj(location) for location in app.data["locations"]}
        self.metrics = {metric["id"]: Metric.parse_obj(metric) for metric in app.data["metrics"]}
        self.device_meta = {
            DOOR_OPEN_ID: DeviceMeta(),
            TEMPERATURE_ID: DeviceMeta(),
            WIFI_STRENGTH_ID: DeviceMeta(),
            WIFI_SSID_ID: DeviceMeta(),
        }
        self.websockets = []

    async def add_connection(self, websocket: WebSocket) -> None:
        self.websockets.append(websocket)

    async def remove_connection(self, websocket: WebSocket) -> None:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            logger.info("Closing websocket ...")
            await websocket.close()
    
    async def start_device(self, device: Device) -> None:
        location = self.locations[device.location_id]
        while True:
            try:
                loop_start = datetime.utcnow()
                next_loop_start = loop_start + timedelta(seconds=random.uniform(*MESSAGE_PERIOD))
                meta = self.device_meta[device.id]
                messages = []

                if meta.reconnect_at is None or meta.reconnect_at < datetime.utcnow():
                    # Maybe send a door open update
                    if meta.last_measurement.get(DOOR_OPEN_ID, datetime(year=2000, month=1, day=1)) + timedelta(seconds=random.uniform(*DOOR_OPEN_UPDATE_PERIOD)) < datetime.utcnow():
                        messages.append(
                            MeasurementMessage(
                                type=MessageTypeEnum.MEASUREMENT,
                                mac=device.mac,
                                metric=self.metrics[DOOR_OPEN_ID].name,
                                value=bool(round(random.random())),
                                tags=[
                                    "door",
                                    "external" if location.name == "Lobby" else "internal",
                                    "workspace" if location.name == "Office" else "other_space",
                                ]
                            )
                        )
                        meta.last_measurement[DOOR_OPEN_ID] = datetime.utcnow()

                    # Maybe send a temperature update
                    if meta.last_measurement.get(TEMPERATURE_ID, datetime(year=2000, month=1, day=1)) + timedelta(seconds=random.uniform(*TEMPERATURE_UPDATE_PERIOD)) < datetime.utcnow():
                        messages.append(
                            MeasurementMessage(
                                type=MessageTypeEnum.MEASUREMENT,
                                mac=device.mac,
                                metric=self.metrics[TEMPERATURE_ID].name,
                                value=round(random.uniform(*TEMPERATURE_RANGE), 1),
                                tags=[
                                    "environment",
                                    "external" if location.name == "Lobby" else "internal",
                                    "workspace" if location.name == "Office" else "other_space",
                                ]
                            )
                        )
                        meta.last_measurement[TEMPERATURE_ID] = datetime.utcnow()

                    # Maybe send a ssid update
                    if meta.last_measurement.get(WIFI_SSID_ID, datetime(year=2000, month=1, day=1)) + timedelta(seconds=random.uniform(*WIFI_SSID_UPDATE_PERIOD)) < datetime.utcnow():
                        messages.append(
                            MeasurementMessage(
                                type=MessageTypeEnum.MEASUREMENT,
                                mac=device.mac,
                                metric=self.metrics[WIFI_SSID_ID].name,
                                value=random.choice(WIFI_SSID_OPTIONS),
                                tags=[
                                    "wifi",
                                    "external" if location.name == "Lobby" else "internal",
                                    "workspace" if location.name == "Office" else "other_space",
                                ]
                            )
                        )
                        meta.last_measurement[WIFI_SSID_ID] = datetime.utcnow()

                    # Maybe send a strength update
                    if meta.last_measurement.get(WIFI_STRENGTH_ID, datetime(year=2000, month=1, day=1)) + timedelta(seconds=random.uniform(*WIFI_STRENGTH_UPDATE_PERIOD)) < datetime.utcnow():
                        messages.append(
                            MeasurementMessage(
                                type=MessageTypeEnum.MEASUREMENT,
                                mac=device.mac,
                                metric=self.metrics[WIFI_STRENGTH_ID].name,
                                value=round(random.uniform(*WIFI_STRENGTH_RANGE), 1),
                                tags=[
                                    "wifi",
                                    "external" if location.name == "Lobby" else "internal",
                                    "workspace" if location.name == "Office" else "other_space",
                                ]
                            )
                        )
                        meta.last_measurement[WIFI_STRENGTH_ID] = datetime.utcnow()

                    # Send ping if no measurements
                    if not messages:
                        messages.append(PingMessage(type=MessageTypeEnum.PING, mac=device.mac))
                    
                    # Randomly disconnect device
                    if random.random() < DEVICE_DISCONNECT_RATE:
                        messages.append(ErrorMessage(type=MessageTypeEnum.ERROR, mac=device.mac, message='disconnected'))
                        meta.reconnect_at = datetime.utcnow() + timedelta(seconds=random.uniform(*DEVICE_DISCONNECT_PERIOD ))

                    # Send messages
                    for message in messages:
                        for websocket in self.websockets:
                            try:
                                if websocket.client_state == WebSocketState.CONNECTED:
                                    await websocket.send_json(message.serialise())
                            except:
                                self.remove_connection(websocket)
                            await asyncio.sleep(random.uniform(*MESSAGE_GAP))

                # Delay between devices
                await asyncio.sleep((next_loop_start - datetime.utcnow()).total_seconds())
            

            except Exception as error:
                raise error

    async def start(self) -> None:
        for device in self.devices.values():
            asyncio.create_task(self.start_device(device))

        while True:
            try:
                websockets_to_remove = []
                for index, websocket in enumerate(self.websockets):
                    # Remove dead websockets
                    if (
                        websocket.client_state not in (WebSocketState.CONNECTING, WebSocketState.CONNECTED) and 
                        index not in websockets_to_remove
                    ):
                        websockets_to_remove.append(index)
                        continue
                    
                    # Randomly close websockets
                    if (
                        random.random() < DISCONNECT_RATE and 
                        index not in websockets_to_remove
                    ):
                        await self.remove_connection(websocket)
                        websockets_to_remove.append(index)
                        continue
                        
                for index in websockets_to_remove:
                    del self.websockets[index]
                
                await asyncio.sleep(random.uniform(*MESSAGE_PERIOD))

            except Exception as error:
                logger.error(error)
                break