# src/config.py

AWS_HOST = "a2olfniwa3qdce-ats.iot.us-east-1.amazonaws.com"
AWS_PORT = 8883  # MQTT over TLS

AWS_ROOT_CA = 'certs/aws_root.pem.pem'
AWS_CLIENT_CERT = 'certs/aws_client.crt.crt'
AWS_PRIVATE_KEY = 'certs/aws_private.key.key'

CLIENT_ID = "Group_05_pi"
TOPIC = "iot/flood_monitor/Group_05/data"

DEVICE_ID = "Group_05"

CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
