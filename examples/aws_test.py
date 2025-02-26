import usr.aws as aws
import modem
import ujson
import sim  #check if pin verification is needed for your sim card, before running the script
import net

# certificate.pem.crt
certificate_content = """
-----BEGIN CERTIFICATE-----

-----END CERTIFICATE-----
"""
# private key
private_content = """
-----BEGIN RSA PRIVATE KEY-----

-----END RSA PRIVATE KEY-----
"""


# device name
client_id = 'qpthing'
# server address
server = 'abgka7vzgjoa0-ats.iot.eu-west-3.amazonaws.com'
# port
port = 8883


def aws_callback(data):
     """
     aws callback
     make your callback here
     """
     print("HELLO from 1234 topic callback")
   
def shadow_callback_get(data):
     """
     aws shadow callback
     make your callback here
     """
     print(" HELLO from get accepted callback")
     
def shadow_callback_update(data):
     """
     aws shadow callback
     make your callback here
     """
     print(" HELLO from update accepted callback")
     
def shadow_callback_delta(data):
     """
     aws shadow callback
     make your callback here
     """
     print(" ELLO from update delta callback")
     
# create aws obj
aws_obj = aws.Aws(client_id, server, port, keep_alive=60,ssl=True,ssl_params={"cert": 
certificate_content,"key": private_content})
print("create aws obj")

# connect mqtt server
print("aws connect start")
aws_obj.connect()
print("aws connect end")

# register callback for '1234' topic
aws_obj.set_callback("1234",aws_callback)
print("aws set callback")

 #subscribe server topic
aws_obj.subscribe("1234")
print("aws subscribe")



#publish to 7777 topic. Subscribe from AWS Console -> MQTT Client before running the script, to see the messsage.
aws_obj.publish("7777","Hello from QuecPython")

aws_obj.start()


'''
    SHADOWS
    
'''

#creating unnamed shadow with default state
aws_obj.create_shadow()

#connecting shadow by subscribing it to all topics 
aws_obj.connect_shadow()

aws_obj.set_callback("$aws/things/qpthing/shadow/get/accepted",shadow_callback_get)
print("shadow_callback_get_accepted_set")

aws_obj.set_callback("$aws/things/qpthing/shadow/update/accepted",shadow_callback_update)
print("shadow_callback_update_accepted_set")

aws_obj.set_callback("$aws/things/qpthing/shadow/update/accepted",shadow_callback_delta)
print("shadow_callback_delta_set")

#using get on unnamed shadow
aws_obj.get_shadow()

#using update on unnamed shadow
aws_obj.update_shadow(state={"state":{"reported":{"welcome": "change reported"}}})


