# src/mqtt_client.py

import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import src.config as config

def create_mqtt_client():
    client = AWSIoTMQTTClient(config.CLIENT_ID)
    client.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
    client.configureCredentials(
        config.AWS_ROOT_CA,
        config.AWS_PRIVATE_KEY,
        config.AWS_CLIENT_CERT
    )

    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
    client.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)

    return client

def publish_sample(client, payload: dict):
    client.publish(config.TOPIC, json.dumps(payload), 1)
