import logging
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import mysql.connector

import MqttConnector
import Authenticator
from SessionManager import SessionManager
from KekboTools import *

app = FastAPI()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class PublishMessage(BaseModel):
    topic: str
    message: str

# Define MQTT broker connection settings
BROKER_DOCKER_HOST = "mosquitto"
BROKER_DOCKR_PORT = 9001 

BROKER_NATIVE_HOST = "localhost"
BROKER_NATIVE_PORT = 9001

# Initialize the MQTT client
if running_in_docker():
    mqtt_client = MqttConnector.MqttConnector(BROKER_DOCKER_HOST, BROKER_DOCKR_PORT)
    dbconn = mysql.connector.connect(
        host = BROKER_DOCKER_HOST,
        user = "root",
        password = "rootpassword",
        database = "yourdatabase",
        charset = 'utf8mb4',
        collation = 'utf8mb4_unicode_ci')
else:
    mqtt_client = MqttConnector.MqttConnector(BROKER_NATIVE_HOST, BROKER_NATIVE_PORT)
    dbconn = mysql.connector.connect(
        host = BROKER_NATIVE_HOST,
        user = "root",
        password = "rootpassword",
        database = "yourdatabase",
        charset = 'utf8mb4',
        collation = 'utf8mb4_unicode_ci')

sessions = SessionManager()

@app.get("/status")
async def status():
    info = {}
    info["session_count"] = sessions.get_session_count()
    return info

async def on_message(websocket, data):
    logger.debug(f"Received: {data}")
    message = json.loads(data)
    if message["action"] == "login":
        auth = Authenticator.Authenticator()
        if auth.authenticate(message['username'], message['password']):
            logger.debug(f"Logging in as {message['username']}")
            sessions.add_session(message['username'])
            await websocket.send_text('{"status": "success"}')
        else:
            logger.debug(f"Failed to login as {message['username']}")
            sessions.remove_session(message['username'])
            await websocket.send_text('{"status": "failed"}')
    elif message["action"] == "logout":
        logger.debug(f"Logging out")
        await websocket.send_text('{"status": "success"}')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.debug("WebSocket connection established")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Received: {data}")
            if not is_valid_json(data):
                await websocket.send_text('{"status": "failed"}')
                continue
            await on_message(websocket, data)
    except WebSocketDisconnect:
        logger.info("WebSocketDisconnect")
    except Exception as e:
        logger.error(f"Exception: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    