import paho.mqtt.client as mqtt
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the incoming POST request
class PublishMessage(BaseModel):
    topic: str
    message: str

# Define MQTT broker connection settings
BROKER_HOST = "mosquitto"  # The hostname is the Docker service name
BROKER_PORT = 9001         # MQTT over WebSockets port

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe("test/topic")  # Subscribe to a topic for testing
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

# Initialize the MQTT client
mqtt_client = mqtt.Client(transport="websockets")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(BROKER_HOST, BROKER_PORT, 60)

# Start the MQTT client loop in the background
mqtt_client.loop_start()

@app.get("/helloworld")
async def helloworld():
    return {"message": "Hello World"}

# Use the Pydantic model to validate the request body
@app.post("/publish")
async def publish_message(data: PublishMessage):
    mqtt_client.publish(data.topic, data.message)
    return {"status": "Message published"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    