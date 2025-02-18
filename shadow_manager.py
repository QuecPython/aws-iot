import ujson
import log

class ShadowManager:
    def __init__(self, mqtt_client, client_id):
        self.mqtt_client = mqtt_client
        self.client_id = client_id
        self.logging = log.getLogger("Shadow")
        self.existing_shadows = set()
        self.unnamed_shadow_used = 0  # 1 if unnamed shadow is already used, 0 otherwise

    def create_shadow(self, state, shadow_name="", state_type="reported"):
        if not shadow_name:
            if self.unnamed_shadow_used:
                self.logging.error("Unnamed shadow is already in use.")
                return
            self.unnamed_shadow_used = 1
        else:
            if shadow_name in self.existing_shadows:
                self.logging.error("Shadow '%s' already exists", shadow_name)
                return
            self.existing_shadows.add(shadow_name)

        self.update_shadow(shadow_name, state, state_type)
        self.logging.info("Shadow '%s' created", shadow_name if shadow_name else "Unnamed")

    def update_shadow(self, shadow_name, state, state_type="reported"):
        if not isinstance(state, dict):
            self.logging.error("State must be a dictionary")
            return

        if state_type not in ["reported", "desired"]:
            self.logging.error("Invalid state type: %s", state_type)
            return

        payload = {"state": {state_type: state}}
        shadow_topic = "$aws/things/{}/shadow".format(self.client_id)
        if shadow_name:
            shadow_topic += "/name/{}".format(shadow_name)
        self.mqtt_client.publish("{}/update".format(shadow_topic), ujson.dumps(payload))

    def get_shadow(self, shadow_name):
        shadow_topic = "$aws/things/{}/shadow".format(self.client_id)
        if shadow_name:
            shadow_topic += "/name/{}".format(shadow_name)
        self.mqtt_client.publish("{}/get".format(shadow_topic), "{}")

    def delete_shadow(self, shadow_name=""):
        shadow_topic = "$aws/things/{}/shadow".format(self.client_id)
        if shadow_name:
            shadow_topic += "/name/{}".format(shadow_name)
        self.mqtt_client.publish("{}/delete".format(shadow_topic), "")

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