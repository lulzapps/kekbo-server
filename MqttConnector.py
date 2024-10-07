import paho.mqtt.client as mqtt
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class MqttConnector:
    def __init__(self, broker_host, broker_port):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.__client = mqtt.Client(transport="websockets")
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
        self.__client.connect(self.broker_host, self.broker_port, 60)
        self.__client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        logger.debug(f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}")
        if rc == 0:
            logger.info(f"Successfully connected to MQTT broker")
            client.subscribe("test/topic")  # Subscribe to a topic for testing
        else:
            logger.error(f"Failed to connect to MQTT broker with return code {rc}")

    def on_message(self, client, userdata, msg):
        logger.debug(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    def publish_message(self, topic, message):
        self.__client.publish(topic, message)
        return {"status": "Message published"}