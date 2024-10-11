import os
import logging
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

import MqttConnector
import Authenticator

app = FastAPI()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class PublishMessage(BaseModel):
    topic: str
    message: str

def running_in_docker():
    if os.path.exists("/.dockerenv"):
        return True
    try:
        with open("/proc/1/cgroup", "rt") as f:
            for line in f:
                if "docker" in line:
                    return True
    except FileNotFoundError:
        pass
    return False

# Define MQTT broker connection settings
BROKER_DOCKER_HOST = "mosquitto"
BROKER_DOCKR_PORT = 9001 

BROKER_NATIVE_HOST = "localhost"
BROKER_NATIVE_PORT = 9001

# Initialize the MQTT client
if running_in_docker():
    mqtt_client = MqttConnector.MqttConnector(BROKER_DOCKER_HOST, BROKER_DOCKR_PORT)
else:
    mqtt_client = MqttConnector.MqttConnector(BROKER_NATIVE_HOST, BROKER_NATIVE_PORT)

@app.get("/helloworld")
async def helloworld():
    return {"message": "Hello World"}

# Use the Pydantic model to validate the request body
@app.post("/publish")
async def publish_message(data: PublishMessage):
    mqtt_client.publish_message(data.topic, data.message)
    return {"status": "Message published"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.debug("WebSocket connection established")
    await websocket.accept()
    try:
        while True:
            logger.debug("waiting for text")
            data = await websocket.receive_text()
            logger.debug(f"Received: {data}")

            # parse the received message into json
            message = json.loads(data)
            if message["action"] == "login":
                auth = Authenticator.Authenticator()
                if auth.authenticate(message['username'], message['password']):
                    logger.debug(f"Logging in as {message['username']}")
                    await websocket.send_text('{"status": "success"}')
                else:
                    logger.debug(f"Failed to login as {message['username']}")
                    await websocket.send_text('{"status": "failed"}')
    except WebSocketDisconnect:
        logger.info("WebSocketDisconnect")
    except Exception as e:
        logger.error(f"Exception: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    