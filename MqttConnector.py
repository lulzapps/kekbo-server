import paho.mqtt.client as mqtt

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
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe("test/topic")  # Subscribe to a topic for testing
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    def publish_message(self, topic, message):
        self.__client.publish(topic, message)
        return {"status": "Message published"}