from usr.mqtt_client import MQTTClientWrapper
from usr.shadow_manager import ShadowManager
import log

__all__ = ['Aws']

class Aws(object):
    """
    AWS IoT Core client
    """
    def __init__(self, client_id, server, port, keep_alive=60, ssl=False, ssl_params=None):
        self.client_id = client_id
        self.mqtt_client = MQTTClientWrapper(client_id, server, port, keep_alive, ssl, ssl_params)
        self.shadow_manager = ShadowManager(self.mqtt_client, client_id)
        self.logging = log.getLogger("AWS")

    def connect(self):
        self.mqtt_client.connect()

    def disconnect(self):
        self.mqtt_client.disconnect()

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic)

    def publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload)

    def create_shadow(self, state, shadow_name="", state_type="reported"):
        self.shadow_manager.create_shadow(state, shadow_name, state_type)

    def update_shadow(self, shadow_name, state, state_type="reported"):
        self.shadow_manager.update_shadow(shadow_name, state, state_type)

    def get_shadow(self, shadow_name):
        self.shadow_manager.get_shadow(shadow_name)

    def delete_shadow(self, shadow_name=""):
        self.shadow_manager.delete_shadow(shadow_name)

    def connect_shadow(self, shadow_name="", topics=None):
        self.shadow_manager.connect_shadow(shadow_name, topics)

    def set_callback(self, topic_name, callback):
        self.mqtt_client.set_callback(topic_name,callback)

    def loop(self):
        self.mqtt_client.loop()

    def start(self):
        self.mqtt_client.start()
