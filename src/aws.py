from usr.mqtt_client import MQTTClientWrapper
from usr.shadow_manager import ShadowManager
import log

__all__ = ['Aws']

class Aws(object):
    """
    AWS IoT Core client
    """
    def __init__(self, client_id, server, port, keep_alive=60, ssl=False, ssl_params=None):
        self.client_id = client_id                                                                     # Client id is a name of the thing 
        self.mqtt_client = MQTTClientWrapper(client_id, server, port, keep_alive, ssl, ssl_params)     # Object for using mqtt 
        self.shadow_manager = ShadowManager(self.mqtt_client, client_id)                               # Object for using shadows feature
        self.logging = log.getLogger("AWS")

    # Used for connecting to AWS IoT Core (server)
    def connect(self):
        self.mqtt_client.connect()

    # Used for disconnecting from server
    def disconnect(self):
        self.mqtt_client.disconnect()

    # Used for subscribing to MQTT topic
    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic)

    # Used for publishing to MQTT topic
    def publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload)


    ''' 
        Shadow feature methods

        If user doesn't enter shadow name, unnamed shadow is used.
        If user doesn't enter state, deafult state will be used. 
        
        *Exception is update state method in which user has to add both.*

    '''
    # Creating shadow method
    def create_shadow(self, shadow_name="",state=""):
        self.shadow_manager.create_shadow(shadow_name,state)

    # Updating shadow method
    def update_shadow(self, shadow_name="", state=""):
        self.shadow_manager.update_shadow(shadow_name, state)

    # Get shadow method 
    def get_shadow(self, shadow_name=""):
        self.shadow_manager.get_shadow(shadow_name)

    # Delete shadow method
    def delete_shadow(self, shadow_name=""):
        self.shadow_manager.delete_shadow(shadow_name)

    # Connect shadow method
    def connect_shadow(self, shadow_name="", topics=None):
        self.shadow_manager.connect_shadow(shadow_name, topics)

    # Set callback method
    def set_callback(self, topic_name, callback):
        self.mqtt_client.set_callback(topic_name,callback)

    def loop(self):
        self.mqtt_client.loop()

    def start(self):
        self.mqtt_client.start()
