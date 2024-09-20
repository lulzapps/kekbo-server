from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import MqttConnector
import os
import logging

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
    print("WebSocket connection established")
    await websocket.accept()
    try:
        while True:
            print("waiting for text")
            data = await websocket.receive_text()
            logger.debug(f"Received: {data}")
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.info("WebSocket connection disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    