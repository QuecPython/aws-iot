import ujson
import log
import utime

class ShadowManager:
    def __init__(self, mqtt_client, client_id):
        self.mqtt_client = mqtt_client
        self.client_id = client_id
        self.logging = log.getLogger("Shadow")
        self.existing_shadows = set()
        self.old_callbacks = {}
        self.accepted_topic = ''
        self.rejected_topic = ''

    # Creating shadow
    def create_shadow(self, shadow_name="", state=""):
        if not state:
            state = {"state":{"desired": {"welcome": "aws-iot"},"reported": {"welcome": "aws-iot"}}}    #default state

        if not shadow_name:
            #callback used to for shadow existance check. Shadow exists -> state exists.
            def shadow_check_callback(payload):
                if "state" in payload:
                    self.logging.error("Unnamed shadow already exists.")
                else:
                    self.update_shadow("", state)
                    self.logging.info("Unnamed shadow created.")
                    
                if self.old_callbacks:
                    self.mqtt_client.callbacks[self.accepted_topic] = self.old_callbacks[self.accepted_topic]
                    self.mqtt_client.callbacks[self.rejected_topic] = self.old_callbacks[self.rejected_topic]
                
                del self.old_callbacks[self.accepted_topic]
                del self.old_callbacks[self.rejected_topic]
                    
            self.get_shadow(shadow_name,callback=shadow_check_callback)
            utime.sleep(2)  # Wait for AWS response
        else:
            self.update_shadow(shadow_name, state)
            if shadow_name:
                self.logging.info("Shadow '{}' updated.".format(shadow_name))
            else:
                self.logging.info("Shadow '{}' created.".format(shadow_name))

    #update shadow used for updating(if called from create shadow then used as a create shadow mechanism)
    def update_shadow(self, shadow_name, state):
        if not state:
            self.logging.error("Enter state then try again")
            return
        if isinstance(state, dict):
            state = ujson.dumps(state)  # Convert dict to JSON string if needed
        elif not isinstance(state, str):
            self.logging.error("State must be a dictionary or a JSON string")
            return

        shadow_topic = "$aws/things/{}/shadow".format(self.client_id)
        print(shadow_topic)
        if shadow_name:
            shadow_topic += "/name/{}".format(shadow_name)
        
        self.mqtt_client.publish("{}/update".format(shadow_topic), state)

    # Get shadow state. Accepted and rejected topic used from 
    def get_shadow(self, shadow_name="",callback=None):
        shadow_topic = "$aws/things/{}/shadow".format(self.client_id)
        if shadow_name:
            shadow_topic += "/name/{}".format(shadow_name)
        
        #if callback exists it means we are here from create shadow method
        if callback:
            self.accepted_topic = "{}/get/accepted".format(shadow_topic)
            self.rejected_topic = "{}/get/rejected".format(shadow_topic)

            #if callback on our topic already exist store it temporarly in old_callbacks dictionary, thus we don't block users callback 
            if self.accepted_topic in self.mqtt_client.callbacks:
                self.old_callbacks[self.accepted_topic] = self.mqtt_client.callbacks[self.accepted_topic]
            if self.rejected_topic in self.mqtt_client.callbacks:
                self.old_callbacks[self.rejected_topic] = self.mqtt_client.callbacks[self.rejected_topic]

            self.mqtt_client.callbacks[self.accepted_topic] = callback
            self.mqtt_client.callbacks[self.rejected_topic] = callback

            self.mqtt_client.subscribe(self.accepted_topic)
            self.mqtt_client.subscribe(self.rejected_topic)
        
        self.mqtt_client.publish("{}/get".format(shadow_topic), "")
        
    # Deletes the shadow based on a shadow name
    def delete_shadow(self, shadow_name=""):
        shadow_topic = "$aws/things/{}/shadow".format(self.client_id)
        if shadow_name:
            shadow_topic += "/name/{}".format(shadow_name)
        self.mqtt_client.publish("{}/delete".format(shadow_topic), "")

    # Connects to all topics if user don't specify topics
    def connect_shadow(self, shadow_name="", topics=None):
        base_topic = "$aws/things/{}/shadow".format(self.client_id)
        if shadow_name:
            base_topic += "/name/{}".format(shadow_name)

        available_topics = {
            "get_accepted": "{}/get/accepted".format(base_topic),
            "get_rejected": "{}/get/rejected".format(base_topic),
            "update_accepted": "{}/update/accepted".format(base_topic),
            "update_rejected": "{}/update/rejected".format(base_topic),
            "update_delta": "{}/update/delta".format(base_topic),
            "update_document": "{}/update/documents".format(base_topic),
            "delete_accepted": "{}/delete/accepted".format(base_topic),
            "delete_rejected": "{}/delete/rejected".format(base_topic)
        }

        if topics is None:
            topics = available_topics.keys()

        if shadow_name not in self.mqtt_client.shadow_topics:
            self.mqtt_client.shadow_topics[shadow_name] = []

        for topic in topics:
            if topic in available_topics:
                self.mqtt_client.subscribe(available_topics[topic])
                self.mqtt_client.shadow_topics[shadow_name].append(available_topics[topic])
            else:
                self.logging.warning("Invalid shadow topic: %s", topic)