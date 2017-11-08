# mqtt.py
# Interface to the MQTT functionality
# Requires pip install paho-mqtt
import paho.mqtt.client as mqtt
import secrets
from singleton import Singleton
from utility import Utility

@Singleton
class ColorManager:
    def __init__(self):
        self.pulseEffectTranslations = {"pulse", "freakout", "chaos"}
        self.colorRotateEffectTranslations = {"rotate", "loop"}

    @staticmethod
    def changeColor(targetColor):
        MQTTInterface.publishMessage(secrets.MQTT_COLOR_TOPIC, targetColor)

    def changeColorHex(self, targetHex):
        value = targetHex.lstrip('#')
        util = Utility()
        hex = util.hex_to_rgb(value)
        strHex = str(hex[0]) + "," + str(hex[1]) + "," + str(hex[2])
        MQTTInterface.publishMessage(secrets.MQTT_COLOR_HEX_TOPIC, strHex)

    def changeColorEffect(self, targetEffect):
        # Check if loop
        if targetEffect in self.colorRotateEffectTranslations:
            MQTTInterface.publishMessage(secrets.MQTT_EFFECT_TOPIC, "lifx_effect_colorloop")
        elif targetEffect in self.pulseEffectTranslations:
            MQTTInterface.publishMessage(secrets.MQTT_EFFECT_TOPIC, "lifx_effect_pulse")

    @staticmethod
    def help():
        return "Use !colorchange to set the mood. Specify either a CSS3 color name of hex value after the command and watch the magic. !colorchange red || !colorchange #Ff0000"

class MQTTInterface:
    
    @staticmethod
    def publishMessage(topic, message):
        client = mqtt.Client("matroxbot")
        client.username_pw_set(secrets.MQTT_USERNAME,secrets.MQTT_PASSWORD)
        client.connect(secrets.MQTT_BROKER_ADDRESS)
        client.publish(topic, message)
